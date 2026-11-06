from transformers import AutoModelForTokenClassification, AutoTokenizer, pipeline

model_path = "./outputs/models/roberta-pii-test"

try:
    model = AutoModelForTokenClassification.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained("roberta-base")

    # aggregation_strategy="simple" bashkon nën-fjalët e prera (p.sh. An + na = Anna)
    nlp_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")

    teksti_test = "Hello, my name is Anna Smith. You can reach me at anna.smith@gmail.com or call me at +355691234567. I live at 123 Main Street, New York."

    print(f'"{teksti_test}"\n')
    rezultatet = nlp_pipeline(teksti_test)

    if len(rezultatet) == 0:
        print("Modeli nuk gjeti asnjë të dhënë sensitive në këtë tekst.")
    else:
        print(f"{'FJALA':<25} | {'ETIKETA PII':<20} | {'BESUESHMËRIA'}")
        print("-" * 70)
        for ent in rezultatet:
            if ent['entity_group'] != 'O':
                print(f"{ent['word']:<25} | {ent['entity_group']:<20} | {ent['score']:.2%}")

except Exception as e:
    print("Modeli ende nuk ka përfunduar trajnimin, ose shtegu i modelit është gabim:", e)
