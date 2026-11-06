import pandas as pd
import ast
from transformers import AutoTokenizer

file_path = "data/raw/pii_dataset.csv"
df = pd.read_csv(file_path)

fjalet = ast.literal_eval(df['tokens'].iloc[0])
etiketat = ast.literal_eval(df['labels'].iloc[0])

print("Fjalët:", fjalet[:10])
print("Etiketat:", etiketat[:10])

tokenizer = AutoTokenizer.from_pretrained("roberta-base")
tokenized_input = tokenizer(fjalet, is_split_into_words=True)
roberta_tokens = tokenizer.convert_ids_to_tokens(tokenized_input["input_ids"])

print("Nën-fjalët e RoBERTa-s:", roberta_tokens[:15])
