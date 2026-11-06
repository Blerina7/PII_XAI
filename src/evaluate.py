import numpy as np
import pandas as pd
from transformers import AutoModelForTokenClassification, AutoTokenizer, Trainer
from datasets import Dataset
import evaluate

model_path = "./outputs/models/roberta-pii-test"
model = AutoModelForTokenClassification.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained("roberta-base")

df = pd.read_json("data/processed/dataseti_gati.json")
dataset = Dataset.from_pandas(df)
eval_dataset = dataset.select(range(200))

metric = evaluate.load("seqeval")

id2label = {
    0: 'O', 1: 'B-EMAIL', 2: 'B-NAME_STUDENT', 3: 'B-PHONE_NUM',
    4: 'B-STREET_ADDRESS', 5: 'B-URL_PERSONAL', 6: 'B-USERNAME',
    7: 'I-NAME_STUDENT', 8: 'I-PHONE_NUM', 9: 'I-STREET_ADDRESS'
}


def compute_metrics(p):
    predictions, labels = p
    predictions = np.argmax(predictions, axis=2)

    true_predictions = [
        [id2label[p] for (p, l) in zip(prediction, label) if l != -100]
        for prediction, label in zip(predictions, labels)
    ]
    true_labels = [
        [id2label[l] for (p, l) in zip(prediction, label) if l != -100]
        for prediction, label in zip(predictions, labels)
    ]

    results = metric.compute(predictions=true_predictions, references=true_labels)
    return {
        "precision": results["overall_precision"],
        "recall": results["overall_recall"],
        "f1": results["overall_f1"],
        "accuracy": results["overall_accuracy"],
    }


trainer = Trainer(
    model=model,
    processing_class=tokenizer,
    compute_metrics=compute_metrics,
)

eval_results = trainer.evaluate(eval_dataset)
for key, value in eval_results.items():
    print(f"{key}: {value:.4f}")
