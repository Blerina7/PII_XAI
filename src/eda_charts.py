import pandas as pd
import ast
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import os

df = pd.read_csv("data/raw/pii_dataset.csv")

te_gjitha_etiketat = []
for labels_str in df['labels']:
    labels = ast.literal_eval(labels_str)
    te_gjitha_etiketat.extend(labels)

etiketat_pii = [label for label in te_gjitha_etiketat if label != 'O']
numerimi = Counter(etiketat_pii)

df_plot = pd.DataFrame.from_dict(numerimi, orient='index').reset_index()
df_plot.columns = ['Lloji i PII', 'Numri i Fjalëve']
df_plot = df_plot.sort_values(by='Numri i Fjalëve', ascending=False)

plt.figure(figsize=(12, 6))
sns.barplot(data=df_plot, x='Numri i Fjalëve', y='Lloji i PII', hue='Lloji i PII', palette='viridis', legend=False)
plt.title('Shpërndarja e të Dhënave Personale (PII) në Dataset', fontsize=16)
plt.xlabel('Numri Total i Fjalëve', fontsize=12)
plt.ylabel('Kategoria', fontsize=12)
plt.grid(axis='x', linestyle='--', alpha=0.7)

os.makedirs("outputs", exist_ok=True)
plt.tight_layout()
plt.savefig("outputs/grafiku_pii.png", dpi=300)
print("Grafiku u ruajt te: outputs/grafiku_pii.png")
