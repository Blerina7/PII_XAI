import pandas as pd
import ast

file_path = "data/raw/pii_dataset.csv"
df = pd.read_csv(file_path)

unique_labels = set()
for labels_str in df['labels']:
    labels_list = ast.literal_eval(labels_str)
    unique_labels.update(labels_list)

# 'O' vendoset e para, pjesa tjetër alfabetikisht
unique_labels = sorted(list(unique_labels))
if 'O' in unique_labels:
    unique_labels.remove('O')
    unique_labels = ['O'] + unique_labels

label2id = {label: i for i, label in enumerate(unique_labels)}
id2label = {i: label for i, label in enumerate(unique_labels)}

print(f"U gjetën {len(unique_labels)} etiketa.")
for label, num in label2id.items():
    print(f"{label:<20} : {num}")
