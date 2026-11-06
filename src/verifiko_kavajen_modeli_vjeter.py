"""
Verifikimi i rastit "Kavajës" me MODELIN E VJETËR (outputs/models/roberta-pii-test), saktësisht si në app.py.
Ekzekutimi (nga dosja XAI_PII, në të njëjtin mjedis ku punonte app.py):
    python src/verifiko_kavajen_modeli_vjeter.py
"""
from transformers import AutoModelForTokenClassification, AutoTokenizer, pipeline

TEKSTI = "Përshëndetje, unë jam Drilona dhe numri im është 0691122334. Jetoj në Rrugën e Kavajës, Tiranë."

LABEL_MAP_APP = {  # fjalori i shkruar me dorë në app.py
    "LABEL_0": "O (Tekst Normal)", "LABEL_1": "B-EMAIL (Email)", "LABEL_2": "B-EMËR (Fillimi i Emrit)",
    "LABEL_3": "B-TELEFON (Fillimi i Numrit)", "LABEL_4": "I-EMËR (Vazhdimi i Emrit)", "LABEL_5": "B-ADRESË (Fillimi i Adresës)",
    "LABEL_6": "I-ADRESË (Vazhdimi i Adresës)", "LABEL_7": "I-EMAIL (Vazhdimi i Emailit)", "LABEL_8": "I-TELEFON (Vazhdimi i Numrit)",
    "LABEL_9": "B-ID (Kartë ID/Pasaportë)"}
HARTA_E_VERTETE = {  # src/labels.py (renditje alfabetike, O në 0)
    "LABEL_0": "O", "LABEL_1": "B-EMAIL", "LABEL_2": "B-NAME_STUDENT", "LABEL_3": "B-PHONE_NUM", "LABEL_4": "B-STREET_ADDRESS",
    "LABEL_5": "B-URL_PERSONAL", "LABEL_6": "B-USERNAME", "LABEL_7": "I-NAME_STUDENT", "LABEL_8": "I-PHONE_NUM", "LABEL_9": "I-STREET_ADDRESS"}

model = AutoModelForTokenClassification.from_pretrained("./outputs/models/roberta-pii-test")
tokenizer = AutoTokenizer.from_pretrained("roberta-base")   # si në app.py

print("=== 1. Si i shfaqte app.py (aggregation_strategy='simple', pa LABEL_0) ===")
for e in pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")(TEKSTI):
    if e["entity_group"] == "LABEL_0":
        continue
    print(f"{e['word']!r:28} {e['entity_group']:8} app.py: {LABEL_MAP_APP[e['entity_group']]:32} "
          f"e vërteta: {HARTA_E_VERTETE[e['entity_group']]:18} p={e['score']:.4f}")

print("\n=== 2. Çdo nën-token veç e veç (pa agregim) ===")
for e in pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="none")(TEKSTI):
    print(f"{e['word']!r:18} {e['entity']:8} app.py: {LABEL_MAP_APP[e['entity']]:32} e vërteta: {HARTA_E_VERTETE[e['entity']]:18} p={e['score']:.4f}")
