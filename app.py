import streamlit as st
from transformers import AutoModelForTokenClassification, AutoTokenizer, pipeline

st.set_page_config(page_title="PII Detektivi (AI)", layout="centered")

st.title("Sistemi i Zbulimit të të Dhënave Personale (PII)")
st.write("Ky aplikacion përdor një model të Inteligjencës Artificiale (RoBERTa) për të gjetur dhe mbrojtur të dhënat e ndjeshme në çdo tekst.")

# Funksioni për të ngarkuar modelin (ruhet në cache që të mos e ngarkojë çdo sekondë)
@st.cache_resource
def load_model():
    model_path = "./outputs/models/roberta-pii-test"
    try:
        model = AutoModelForTokenClassification.from_pretrained(model_path)
        tokenizer = AutoTokenizer.from_pretrained("roberta-base")
        return pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")
    except:
        return None

nlp_pipeline = load_model()

if nlp_pipeline is None:
    st.warning("Modeli nuk është gati! Të lutem përfundo trajnimin (Hapi 5) fillimisht.")
else:
    # Kutia ku do shkruajmë tekstin
    user_input = st.text_area("Shkruaj një tekst për ta analizuar:",
                              "Përshëndetje, unë jam Drilona dhe numri im është 0691122334. Jetoj në Rrugën e Kavajës, Tiranë.")
    
    if st.button("Kërko për PII"):
        with st.spinner("Modeli po mendon..."):
            rezultatet = nlp_pipeline(user_input)
            
# Filtrojmë: mbajmë VETËM ato që nuk janë LABEL_0 (fjalë normale)
            te_dhena_sensitive = [ent for ent in rezultatet if ent['entity_group'] != 'LABEL_0']
            
            if len(te_dhena_sensitive) == 0:
                st.success("Asnjë e dhënë e ndjeshme nuk u gjet!")
            else:
                # Tani numëron saktë vetëm ato që shfaqen!
                st.error(f"U gjetën {len(te_dhena_sensitive)} të dhëna sensitive:")
                
                label_map = {
                    "LABEL_0": "O (Tekst Normal)",
                    "LABEL_1": "B-EMAIL (Email)",
                    "LABEL_2": "B-EMËR (Fillimi i Emrit)",
                    "LABEL_3": "B-TELEFON (Fillimi i Numrit)",
                    "LABEL_4": "I-EMËR (Vazhdimi i Emrit)",
                    "LABEL_5": "B-ADRESË (Fillimi i Adresës)",
                    "LABEL_6": "I-ADRESË (Vazhdimi i Adresës)",
                    "LABEL_7": "I-EMAIL (Vazhdimi i Emailit)",
                    "LABEL_8": "I-TELEFON (Vazhdimi i Numrit)",
                    "LABEL_9": "B-ID (Kartë ID/Pasaportë)"
                }

                st.markdown("### Të dhënat e zbuluara:")
                for ent in te_dhena_sensitive:
                    emri_bukur = label_map.get(ent['entity_group'], ent['entity_group'])
                    st.markdown(f"**{ent['word']}**  → Kategoria: `{emri_bukur}` | *Saktësia: {ent['score']:.2%}*")