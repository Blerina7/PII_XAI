import pandas as pd, ast, re, random, json, time
import pycrfsuite
from collections import Counter, defaultdict

df = pd.read_csv('data/raw/pii_dataset.csv')
docs = [(ast.literal_eval(t), ast.literal_eval(l)) for t, l in zip(df['tokens'], df['labels'])]
random.seed(42)
idx = list(range(len(docs))); random.shuffle(idx)
cut = int(0.8 * len(idx))
train = [docs[i] for i in idx[:cut]]; test = [docs[i] for i in idx[cut:]]

def spans(labels):
    out = set(); start = None; typ = None
    for i, lab in enumerate(labels + ['O']):
        if lab.startswith('B-') or lab == 'O' or (lab.startswith('I-') and lab[2:] != typ):
            if typ is not None: out.add((start, i, typ))
            start, typ = (i, lab[2:]) if lab != 'O' else (None, None)
    return out

def evaluate(golds, preds):
    tp = Counter(); fp = Counter(); fn = Counter()
    for g, p in zip(golds, preds):
        gs, ps = spans(g), spans(p)
        for s in ps:
            (tp if s in gs else fp)[s[2]] += 1
        for s in gs:
            if s not in ps: fn[s[2]] += 1
    res = {}
    types = sorted(set(tp) | set(fp) | set(fn))
    T = F = N = 0
    for t in types:
        P = tp[t] / (tp[t] + fp[t]) if tp[t] + fp[t] else 0
        R = tp[t] / (tp[t] + fn[t]) if tp[t] + fn[t] else 0
        F1 = 2 * P * R / (P + R) if P + R else 0
        res[t] = dict(P=round(P, 4), R=round(R, 4), F1=round(F1, 4), support=tp[t] + fn[t])
        T += tp[t]; F += fp[t]; N += fn[t]
    P = T / (T + F) if T + F else 0; R = T / (T + N) if T + N else 0
    res['MICRO'] = dict(P=round(P, 4), R=round(R, 4), F1=round(2 * P * R / (P + R), 4) if P + R else 0, support=T + N)
    return res

# ---------- RegEx baseline ----------
EMAIL = re.compile(r'^[\w.+-]+@[\w-]+(\.[\w-]+)+$')
URL = re.compile(r'^(https?://|www\.)\S+$')
PHONEPART = re.compile(r'^[\d()+\-.x]+$')
def regex_tag(tokens):
    labs = ['O'] * len(tokens)
    for i, tok in enumerate(tokens):
        if EMAIL.match(tok): labs[i] = 'B-EMAIL'
        elif URL.match(tok): labs[i] = 'B-URL_PERSONAL'
    i = 0
    while i < len(tokens):
        if PHONEPART.match(tokens[i]) and sum(c.isdigit() for c in tokens[i]) >= 2:
            j = i; digits = 0
            while j < len(tokens) and (PHONEPART.match(tokens[j]) or tokens[j].strip() == ''):
                digits += sum(c.isdigit() for c in tokens[j]); j += 1
            if 7 <= digits <= 15:
                labs[i] = 'B-PHONE_NUM'
                for k in range(i + 1, j): labs[k] = 'I-PHONE_NUM'
            i = j
        else:
            i += 1
    return labs
t0 = time.time()
rx = evaluate([d[1] for d in test], [regex_tag(d[0]) for d in test])
print('REGEX', json.dumps(rx, indent=1), time.time() - t0)

# ---------- CRF baseline ----------
def w2f(toks, i):
    w = toks[i]
    f = {'b': 1.0, 'w.lower': w.lower(), 'suf3': w[-3:], 'pre3': w[:3], 'istitle': w.istitle(),
         'isupper': w.isupper(), 'isdigit': w.isdigit(), 'has@': '@' in w, 'hasdigit': any(c.isdigit() for c in w),
         'shape': re.sub(r'[A-Z]', 'A', re.sub(r'[a-z]', 'a', re.sub(r'\d', '0', w)))[:8], 'len': min(len(w), 10)}
    for off in (-2, -1, 1, 2):
        j = i + off
        if 0 <= j < len(toks):
            v = toks[j]; f[f'{off}:lower'] = v.lower(); f[f'{off}:istitle'] = v.istitle()
        else:
            f[f'{off}:pad'] = True
    return {k: (str(v) if not isinstance(v, (bool, float, int)) or isinstance(v, bool) else v) for k, v in f.items()}

def feats(toks):
    out = []
    for i in range(len(toks)):
        d = {}
        for k, v in w2f(toks, i).items():
            if isinstance(v, str): d[f'{k}={v}'] = 1.0
            else: d[k] = float(v)
        out.append(d)
    return out

t0 = time.time()
tr = pycrfsuite.Trainer(verbose=False)
for toks, labs in train:
    tr.append(pycrfsuite.ItemSequence(feats(toks)), labs)
tr.set_params({'c1': 0.1, 'c2': 0.01, 'max_iterations': 80, 'feature.possible_transitions': True})
tr.train('outputs/models/crf_pii.model')
print('CRF train time', time.time() - t0)
tg = pycrfsuite.Tagger(); tg.open('outputs/models/crf_pii.model')
preds = [tg.tag(pycrfsuite.ItemSequence(feats(d[0]))) for d in test]
crf = evaluate([d[1] for d in test], preds)
print('CRF', json.dumps(crf, indent=1))

# Albanian OOD mini-probe on CRF
alb = ["Përshëndetje , unë jam Drilona Hoxha dhe numri im është 0691122334 . Jetoj në Rrugën e Kavajës , Tiranë .".split(),
       "Mund të më shkruani në drilona.hoxha@gmail.com ose të më telefononi në +355 69 112 2334 .".split(),
       "Studenti Arben Shehu banon në Lagjja 5 Maji , Rruga Gjergj Fishta , Nr. 12 , Durrës .".split()]
for s in alb:
    print(list(zip(s, tg.tag(pycrfsuite.ItemSequence(feats(s))))))
json.dump({'regex': rx, 'crf': crf, 'n_train': len(train), 'n_test': len(test)}, open('outputs/baselines.json', 'w'), indent=1)
