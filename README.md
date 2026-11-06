<div align="center">

#  Explainable PII Detection using NLP Techniques

**Detecting personal data in text with RoBERTa, CRF and explainable AI (XAI)**

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?logo=pytorch&logoColor=white)
![HuggingFace](https://img.shields.io/badge/🤗_Transformers-FFD21E?logoColor=black)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)

</div>

---

##  Overview

This project treats the detection of Personally Identifiable Information (PII) in text as a **Named Entity Recognition (NER)** problem, and pairs every prediction with an **explanation** of why the model assigned a given label to a token.

Three approaches are compared on the same dataset:

| Approach | Role |
| --- | --- |
| **RegEx** | Rule-based baseline: interpretable but brittle |
| **CRF** | Classical statistical sequence model |
| **RoBERTa-base** (fine-tuned) | Main model, trained with early stopping (8 epochs) |

On top of RoBERTa, explainability methods are applied and evaluated with the **ERASER** faithfulness criteria, together with **counterfactual** analysis (how predictions change when the input is altered).

> Roughly 97.1% of all tokens belong to the `O` (non-entity) class, so overall accuracy is misleading. Evaluation relies on per-class precision, recall and F1.

---

##  Features

-  Token-level RoBERTa-base fine-tuning using the BIO tagging scheme
-  RegEx and CRF baselines for comparison
-  Token attribution heatmaps (red = pushes toward the wrong prediction, blue = toward the correct label)
-  Counterfactual tests and error analysis (e.g. Albanian place names misread as other entity types)
-  Interactive **Streamlit** demo (`app.py`, `app_v2.py`)

---

##  Repository structure

> Adjust to match your actual folders.

```
PII_XAI/
├── README.md
├── .gitignore
├── requirements.txt
├── app.py                      # Baseline Streamlit app
├── app_v2.py                   # App using the retrained RoBERTa model
├── data/
│   ├── raw/                    # Original dataset (pii_dataset.csv)
│   └── processed/              # Processed dataset (dataseti_gati.json)
├── outputs/
│   ├── colab_roberta-base_ep8_es/
│   │   ├── xai/                # Explainability heatmaps
│   │   └── model/              # 
│   └── figurat_diplome/        # Figures and plots
├── docs/                       # Report and slides
└── presentation/               # build.js, heat.json
```

---

##  Quick start

### 1. Clone the repository

```bash
git clone https://github.com/Blerina7/PII_XAI.git
cd PII_XAI
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux / macOS

pip install -r requirements.txt
```

### 3. Download the model weights

The weights (~470 MB) exceed GitHub's file size limit. Download them from:


and place them exactly here:

```
outputs/colab_roberta-base_ep8_es/model/
```

The folder must contain `model.safetensors`, `config.json` and the tokenizer files.

### 4. Run the app

```bash
streamlit run app_v2.py
```

The app opens at `http://localhost:8501`. Enter a sentence to see the detected entities along with their explanations.

---

##  Results



| Model | Precision | Recall | F1 |
| --- | --- | --- | --- |
| RegEx | – | – | – |
| CRF | – | – | – |
| **RoBERTa-base** | – | – | – |

Full figures (confusion matrix, heatmaps, counterfactuals) are in `outputs/figurat_diplome/`.

---

##  Method in brief

1. **Data:** labeled text containing PII entities, cleaned and converted to BIO format.
2. **Tokenization:** RoBERTa's Byte-Pair Encoding, with labels aligned at the subword level.
3. **Training:** RoBERTa-base fine-tuned with early stopping, run on Google Colab.
4. **Explainability:** token attribution, ERASER-style faithfulness evaluation and counterfactual tests.
5. **Demo:** Streamlit interface for interactive use.

---

##  Privacy and responsible use

- The project uses **public or synthetic data only**. It contains no real PII.
- The model is a research prototype and **should not be the sole tool** for anonymization in real systems. False negatives can leave personal data exposed.
- Poor recognition of Albanian-specific entities (e.g. addresses) is a known limitation.

---

##  Future work

- Extend the dataset with more Albanian text and local address formats
- Compare against multilingual models (XLM-RoBERTa)
- Run a human study on the quality of the explanations

---

##  Author

**Blerina Tafaj**

##  Citation

```bibtex
@software{tafaj2026piixai,
  author = {Tafaj, Blerina},
  title  = {Explainable PII Detection using NLP Techniques},
  year   = {2026},
  url    = {https://github.com/Blerina7/PII_XAI}
}
```

