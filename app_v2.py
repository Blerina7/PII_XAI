"""
app_v2.py — Ndërfaqja Streamlit me hartën e saktë të etiketave (lexohet nga modeli, jo e shkruar me dorë).
Përdorimi:  streamlit run app_v2.py
Modeli: dosja që prodhon notebook-u i Colab-it (outputs/colab_roberta-base/model), e shkarkuar lokalisht.
"""
import streamlit as st
from transformers import AutoModelForTokenClassification, AutoTokenizer, pipeline

MODEL_PATH = "./outputs/colab_roberta-base_ep8_es/model"   # modeli i run-it të ri (ndalim i hershëm)

EMERTIME = {
    "NAME_STUDENT": "Emër personi",
    "EMAIL": "Email",
    "PHONE_NUM": "Numër telefoni",
    "STREET_ADDRESS": "Adresë",
    "URL_PERSONAL": "URL personale",
    "USERNAME": "Emër përdoruesi",
}
NGJYRA = {
    "NAME_STUDENT": "#fbe3ec", "EMAIL": "#e3f0fb", "PHONE_NUM": "#e6f7e6",
    "STREET_ADDRESS": "#fff3d6", "URL_PERSONAL": "#ece3fb", "USERNAME": "#e3fbf7",
}

st.set_page_config(page_title="Zbulimi i PII", layout="centered")
st.title("Zbulimi i të dhënave personale (PII)")
st.caption("Model RoBERTa i përshtatur për klasifikimin e tokenëve. Etiketat lexohen nga konfigurimi i modelit.")


@st.cache_resource
def load_pipeline():
    model = AutoModelForTokenClassification.from_pretrained(MODEL_PATH)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, add_prefix_space=True)
    # me id2label të ruajtur (p.sh. "B-STREET_ADDRESS"), strategjia "simple" bashkon saktë B- dhe I-
    return pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple"), model.config.id2label


try:
    nlp, id2label = load_pipeline()
except Exception as e:
    st.error(f"Modeli nuk u ngarkua nga {MODEL_PATH}: {e}")
    st.stop()

if any(v.startswith("LABEL_") for v in id2label.values()):
    st.warning("Modeli nuk ka emra etiketash në config.json (LABEL_0…). Ritrajnoje me notebook-un e Colab-it.")

tekst = st.text_area("Teksti për analizë:",
                     "Përshëndetje, unë jam Drilona dhe numri im është 0691122334. Jetoj në Rrugën e Kavajës, Tiranë.",
                     height=140)

if st.button("Kërko për PII"):
    entitetet = [e for e in nlp(tekst) if e["entity_group"] != "O"]
    if not entitetet:
        st.success("Nuk u gjet asnjë e dhënë personale.")
    else:
        # Teksti me theksime
        html, last = "", 0
        for e in sorted(entitetet, key=lambda x: x["start"]):
            html += tekst[last:e["start"]]
            c = NGJYRA.get(e["entity_group"], "#eee")
            html += (f"<span style='background:{c};padding:2px 4px;border-radius:4px'>{tekst[e['start']:e['end']]}"
                     f"<sub style='font-size:0.7em'> {EMERTIME.get(e['entity_group'], e['entity_group'])}</sub></span>")
            last = e["end"]
        html += tekst[last:]
        st.markdown(html, unsafe_allow_html=True)

        st.subheader(f"U gjetën {len(entitetet)} entitete")
        st.table([{"Teksti": tekst[e["start"]:e["end"]],
                   "Kategoria": EMERTIME.get(e["entity_group"], e["entity_group"]),
                   "Etiketa e modelit": e["entity_group"],
                   "Besueshmëria": f"{e['score']:.1%}"} for e in entitetet])