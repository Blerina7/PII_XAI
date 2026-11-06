import pandas as pd
from datasets import Dataset
from transformers import AutoModelForTokenClassification, TrainingArguments, Trainer, DataCollatorForTokenClassification
from transformers import AutoTokenizer

df = pd.read_json("data/processed/dataseti_gati.json")
dataset = Dataset.from_pandas(df)

train_dataset = dataset
eval_dataset = dataset.select(range(200))

model = AutoModelForTokenClassification.from_pretrained("roberta-base", num_labels=10)
tokenizer = AutoTokenizer.from_pretrained("roberta-base")
data_collator = DataCollatorForTokenClassification(tokenizer=tokenizer)

training_args = TrainingArguments(
    output_dir="./outputs/models/roberta-pii-test",
    learning_rate=2e-5,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    num_train_epochs=2,
    weight_decay=0.01,
    eval_strategy="epoch",
    save_strategy="epoch",
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    processing_class=tokenizer,
    data_collator=data_collator,
)

trainer.train()
print("Trajnimi përfundoi. Modeli u ruajt te outputs/models/roberta-pii-test.")
