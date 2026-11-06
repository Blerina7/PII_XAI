import pandas as pd
import ast
from transformers import AutoTokenizer

df = pd.read_csv("data/raw/pii_dataset.csv")
fjalet = ast.literal_eval(df['tokens'].iloc[0])
etiketat = ast.literal_eval(df['labels'].iloc[0])

tokenizer = AutoTokenizer.from_pretrained("roberta-base")

tokenized_input = tokenizer(
    fjalet,
    is_split_into_words=True,
    truncation=True,
    max_length=512
)

roberta_tokens = tokenizer.convert_ids_to_tokens(tokenized_input["input_ids"])
word_ids = tokenized_input.word_ids()  # tregon nga cila fjalë origjinale vjen çdo nën-token

print(f"\n{'Nën-Fjala (Token)':<18} | {'Vjen nga fjala nr.':<18} | {'Etiketa e Re'}")
print("-" * 65)

etiketat_e_reja = []
previous_word_idx = None

for i in range(15):
    word_idx = word_ids[i]
    token_text = roberta_tokens[i]

    if word_idx is None:
        # tokenet speciale <s>/</s>
        label = "-100 (Injorohet)"
    elif word_idx != previous_word_idx:
        label = etiketat[word_idx]
    else:
        # vazhdim i së njëjtës fjalë
        label = "-100 (Vazhdim fjale)"

    previous_word_idx = word_idx
    print(f"{token_text:<18} | {str(word_idx):<18} | {label}")
