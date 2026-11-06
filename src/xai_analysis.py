"""
xai_analysis.py — Vlerësimi i RoBERTa-s dhe analiza e shpjegueshmërisë (XAI)
Punim diplome: Explainable Detection of PII in Text using NLP Techniques

Ekzekutohet në Google Colab (GPU T4) nga rrënja e projektit XAI_PII:
    pip install transformers datasets seqeval shap lime matplotlib
    python src/xai_analysis.py

Çfarë prodhon (në outputs/xai/):
  1. metrics_en.json      – Precision/Recall/F1 mbi test-set-in anglisht (i ndarë, pa rrjedhje të dhënash)
  2. metrics_sq.json      – të njëjtat metrika mbi setin OOD në shqip (data/test_shqip.json)
  3. cm_roberta.png       – matrica e ngatërresave (token-level, tipet e entiteteve)
  4. attention_*.png      – hartat e vëmendjes për shembujt e zgjedhur
  5. occlusion_*.png      – shpjegim me perturbim (LIME-style / occlusion) për një token të caktuar
  6. shap_*.html          – shpjegimet SHAP (nëse biblioteka shap funksionon në mjedis)
"""
import os, json, random
import numpy as np
import torch
import matplotlib.pyplot as plt
from transformers import AutoModelForTokenClassification, AutoTokenizer

MODEL = "./outputs/models/roberta-pii-test"
OUT = "./outputs/xai"
os.makedirs(OUT, exist_ok=True)

# Renditja e etiketave duhet të jetë e njëjtë me src/labels.py dhe src/preprocess.py.
ID2LABEL = {0: 'O', 1: 'B-EMAIL', 2: 'B-NAME_STUDENT', 3: 'B-PHONE_NUM', 4: 'B-STREET_ADDRESS',
            5: 'B-URL_PERSONAL', 6: 'B-USERNAME', 7: 'I-NAME_STUDENT', 8: 'I-PHONE_NUM', 9: 'I-STREET_ADDRESS'}

device = "cuda" if torch.cuda.is_available() else "cpu"
tok = AutoTokenizer.from_pretrained(MODEL, add_prefix_space=True)
model = AutoModelForTokenClassification.from_pretrained(MODEL, output_attentions=True).to(device).eval()


def predict_words(words):
    enc = tok(words, is_split_into_words=True, return_tensors="pt", truncation=True, max_length=512).to(device)
    with torch.no_grad():
        out = model(**enc)
    probs = out.logits.softmax(-1)[0].cpu().numpy()
    wid = enc.word_ids()
    labels, wprobs, seen = ['O'] * len(words), [None] * len(words), set()
    for i, w in enumerate(wid):
        if w is None or w in seen:
            continue
        seen.add(w)
        labels[w] = ID2LABEL[int(probs[i].argmax())]
        wprobs[w] = probs[i]
    return labels, wprobs, enc, out


def spans(labels):
    out, start, typ = set(), None, None
    for i, lab in enumerate(labels + ['O']):
        if lab.startswith('B-') or lab == 'O' or (lab.startswith('I-') and lab[2:] != typ):
            if typ is not None:
                out.add((start, i, typ))
            start, typ = (i, lab[2:]) if lab != 'O' else (None, None)
    return out


def entity_metrics(golds, preds):
    from collections import Counter
    tp, fp, fn = Counter(), Counter(), Counter()
    for g, p in zip(golds, preds):
        gs, ps = spans(g), spans(p)
        for s in ps:
            (tp if s in gs else fp)[s[2]] += 1
        for s in gs:
            if s not in ps:
                fn[s[2]] += 1
    res, T, F, N = {}, 0, 0, 0
    for t in sorted(set(tp) | set(fp) | set(fn)):
        P = tp[t] / max(tp[t] + fp[t], 1); R = tp[t] / max(tp[t] + fn[t], 1)
        res[t] = dict(P=P, R=R, F1=2 * P * R / max(P + R, 1e-9), support=tp[t] + fn[t])
        T += tp[t]; F += fp[t]; N += fn[t]
    P = T / max(T + F, 1); R = T / max(T + N, 1)
    res['MICRO'] = dict(P=P, R=R, F1=2 * P * R / max(P + R, 1e-9), support=T + N)
    return res


# ---------------- 1. Vlerësimi anglisht (ndarje 80/20 me seed 42, si baseline-t CRF) ----------------
import pandas as pd, ast
df = pd.read_csv("data/raw/pii_dataset.csv")
docs = [(ast.literal_eval(t), ast.literal_eval(l)) for t, l in zip(df['tokens'], df['labels'])]
random.seed(42); idx = list(range(len(docs))); random.shuffle(idx)
test = [docs[i] for i in idx[int(0.8 * len(idx)):]]
# SHËNIM: modeli duhet të ritrajnohet VETËM mbi idx[:80%] që këto metrika të jenë të vlefshme.
golds, preds = [], []
for words, labs in test:
    p, _, _, _ = predict_words(words)
    golds.append(labs); preds.append(p)
json.dump(entity_metrics(golds, preds), open(f"{OUT}/metrics_en.json", "w"), indent=1)

# Matrica e ngatërresave
C = ['O', 'NAME_STUDENT', 'EMAIL', 'PHONE_NUM', 'STREET_ADDRESS', 'URL_PERSONAL', 'USERNAME']
M = np.zeros((7, 7), dtype=int)
for g, p in zip(golds, preds):
    for a, b in zip(g, p):
        M[C.index(a[2:] if a != 'O' else 'O'), C.index(b[2:] if b != 'O' else 'O')] += 1
Mn = M / M.sum(1, keepdims=True)
plt.figure(figsize=(6, 5)); plt.imshow(Mn, cmap='Blues', vmin=0, vmax=1)
plt.xticks(range(7), C, rotation=40, fontsize=7); plt.yticks(range(7), C, fontsize=7)
for i in range(7):
    for j in range(7):
        plt.text(j, i, f"{Mn[i, j]:.3f}", ha='center', va='center', fontsize=6)
plt.xlabel('Parashikuar'); plt.ylabel('E vërtetë'); plt.tight_layout(); plt.savefig(f"{OUT}/cm_roberta.png", dpi=200); plt.close()

# ---------------- 2. Vlerësimi OOD shqip ----------------
sq = json.load(open("data/test_shqip.json", encoding="utf-8"))
g2, p2 = [], []
for s in sq:
    p, _, _, _ = predict_words(s['tokens'])
    g2.append(s['labels']); p2.append(p)
json.dump(entity_metrics(g2, p2), open(f"{OUT}/metrics_sq.json", "w"), indent=1)
json.dump([dict(tokens=s['tokens'], gold=g, pred=p) for s, g, p in zip(sq, g2, p2)],
          open(f"{OUT}/predictions_sq.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)


# ---------------- 3. Attention: harta e vëmendjes për fjalinë "Rruga e Kavajës" ----------------
def attention_map(words, layer=-1, name="kavaja"):
    _, _, enc, out = predict_words(words)
    att = out.attentions[layer][0].mean(0).cpu().numpy()  # mesatarja mbi 12 kokat
    toks = tok.convert_ids_to_tokens(enc["input_ids"][0])
    toks = [t.replace('Ġ', '').replace('Ã«', 'ë') for t in toks]
    plt.figure(figsize=(9, 8)); plt.imshow(att, cmap='viridis')
    plt.xticks(range(len(toks)), toks, rotation=90, fontsize=6); plt.yticks(range(len(toks)), toks, fontsize=6)
    plt.title(f"Vëmendja mesatare – shtresa {layer}"); plt.tight_layout()
    plt.savefig(f"{OUT}/attention_{name}_L{layer}.png", dpi=200); plt.close()


example = "Përshëndetje , unë jam Drilona Hoxha dhe numri im është 0691122334 . Jetoj në Rrugën e Kavajës , Tiranë .".split()
for L in (0, 6, 11):
    attention_map(example, layer=L)


# ---------------- 4. Occlusion (perturbim, logjika e LIME) për tokenin "Kavajës" ----------------
def occlusion(words, target_idx, name):
    labels, probs, _, _ = predict_words(words)
    cls = int(np.argmax(probs[target_idx]))
    base = probs[target_idx][cls]
    deltas = []
    for j in range(len(words)):
        if j == target_idx:
            deltas.append(0.0); continue
        w2 = words[:j] + ['<mask>'] + words[j + 1:]
        _, p2, _, _ = predict_words(w2)
        deltas.append(float(base - p2[target_idx][cls]))
    plt.figure(figsize=(9, 3)); plt.bar(range(len(words)), deltas, color=['#d45087' if d > 0 else '#2f4b7c' for d in deltas])
    plt.xticks(range(len(words)), words, rotation=60, fontsize=7)
    plt.ylabel(f"Rënia e P({ID2LABEL[cls]})"); plt.title(f"Occlusion për '{words[target_idx]}'")
    plt.tight_layout(); plt.savefig(f"{OUT}/occlusion_{name}.png", dpi=200); plt.close()
    return dict(word=words[target_idx], predicted=ID2LABEL[cls], p=float(base), deltas=dict(zip(words, deltas)))


json.dump(occlusion(example, example.index('Kavajës'), 'kavaja'), open(f"{OUT}/occlusion_kavaja.json", "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)

# ---------------- 5. SHAP (opsionale) ----------------
try:
    import shap
    target = example.index('Kavajës')

    def f(texts):
        res = []
        for t in texts:
            ws = t.split()
            if len(ws) <= target:
                res.append(np.zeros(len(ID2LABEL))); continue
            _, p, _, _ = predict_words(ws)
            res.append(p[target] if p[target] is not None else np.zeros(len(ID2LABEL)))
        return np.array(res)

    masker = shap.maskers.Text(r"\s+")
    explainer = shap.Explainer(f, masker, output_names=list(ID2LABEL.values()))
    sv = explainer([" ".join(example)])
    open(f"{OUT}/shap_kavaja.html", "w").write(shap.plots.text(sv, display=False))
except Exception as e:
    print("SHAP nuk u ekzekutua:", e)

print("Analiza XAI përfundoi. Rezultatet janë në", OUT)
