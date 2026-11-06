import pandas as pd
import ast
import os
from transformers import AutoTokenizer

file_path = "data/raw/pii_dataset.csv"
df = pd.read_csv(file_path)

unique_labels = set()
for labels_str in df['labels']:
    unique_labels.update(ast.literal_eval(labels_str))

unique_labels = sorted(list(unique_labels))
if 'O' in unique_labels:
    unique_labels.remove('O')
    unique_labels = ['O'] + unique_labels

label2id = {label: i for i, label in enumerate(unique_labels)}
tokenizer = AutoTokenizer.from_pretrained("roberta-base")


def perpunimi_rreshtit(row):
    fjalet = ast.literal_eval(row['tokens'])
    etiketat_tekst = ast.literal_eval(row['labels'])

    tokenized_input = tokenizer(
        fjalet,
        is_split_into_words=True,
        truncation=True,
        max_length=512
    )

    word_ids = tokenized_input.word_ids()
    etiketat_numra = []
    previous_word_idx = None

    for word_idx in word_ids:
        if word_idx is None:
            etiketat_numra.append(-100)
        elif word_idx != previous_word_idx:
            label_tekst = etiketat_tekst[word_idx]
            etiketat_numra.append(label2id[label_tekst])
        else:
            etiketat_numra.append(-100)
        previous_word_idx = word_idx

    return {
        "input_ids": tokenized_input["input_ids"],
        "attention_mask": tokenized_input["attention_mask"],
        "labels": etiketat_numra
    }


te_dhenat_e_gati = df.apply(perpunimi_rreshtit, axis=1).tolist()
processed_df = pd.DataFrame(te_dhenat_e_gati)

os.makedirs("data/processed", exist_ok=True)
out_path = "data/processed/dataseti_gati.json"
processed_df.to_json(out_path, orient='records')

print(f"Të dhënat u përpunuan dhe u ruajtën te: {out_path}")
