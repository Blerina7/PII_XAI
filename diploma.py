from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_LEADER, WD_TAB_ALIGNMENT

def shto_titull_qender(doc, tekst, madhesia, bold=True):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(tekst)
    run.bold = bold
    run.font.name = 'Times New Roman'
    run.font.size = Pt(madhesia)
    run.font.color.rgb = RGBColor(0, 0, 0)
    return p

def shto_titull_kapitulli(doc, tekst):
    doc.add_page_break()
    p = doc.add_heading(tekst, level=1)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.runs[0]
    run.font.name = 'Times New Roman'
    run.font.size = Pt(14)
    run.font.color.rgb = RGBColor(0, 0, 0)
    run.bold = True
    doc.add_paragraph()

def shto_nen_titull(doc, tekst, niveli=2):
    p = doc.add_heading(tekst, level=niveli)
    run = p.runs[0]
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run.font.color.rgb = RGBColor(0, 0, 0)
    run.bold = True
    doc.add_paragraph()

def shto_tekst(doc, teksti):
    p = doc.add_paragraph()
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    run = p.add_run(teksti)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run.font.color.rgb = RGBColor(0, 0, 0)
    doc.add_paragraph()

def shto_rresht_toc(doc, titulli, faqja, bold=False, indent=0):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(indent)
    tab_stops = p.paragraph_format.tab_stops
    tab_stops.add_tab_stop(Inches(6.0), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
    run = p.add_run(f"{titulli}\t{faqja}")
    run.bold = bold
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run.font.color.rgb = RGBColor(0, 0, 0)

doc = Document()

for section in doc.sections:
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.5)
    section.right_margin = Inches(1.0)

# --- KOPERTINA ---
shto_titull_qender(doc, "REPUBLIKA E SHQIPËRISË", 14)
shto_titull_qender(doc, "UNIVERSITETI POLITEKNIK I TIRANËS", 14)
shto_titull_qender(doc, "FAKULTETI I TEKNOLOGJISË SË INFORMACIONIT", 14)
shto_titull_qender(doc, "Departamenti i Inxhinierisë Kompjuterike", 14)
doc.add_paragraph("\n\n")
shto_titull_qender(doc, "PUNIM DIPLOME", 14)
doc.add_paragraph("\n")
shto_titull_qender(doc, "Zbulimi i të Dhënave Personale (PII) në Tekste duke Përdorur Arkitekturën RoBERTa: Analizë, Implementim dhe Vlerësim", 16)
doc.add_paragraph("\n\n\n")
shto_titull_qender(doc, "Punoi: Blerina Tafaj", 14, bold=False)
shto_titull_qender(doc, "Udhëheqës Shkencor: [Titulli akademik + Emri Mbiemri]", 14, bold=False)
shto_titull_qender(doc, "Dega: Inxhinieri Kompjuterike", 14, bold=False)
doc.add_paragraph("\n\n\n")
shto_titull_qender(doc, "Tiranë, 2026", 12)

# --- DEKLARATË ORIGJINALITETI ---
doc.add_page_break()
shto_titull_qender(doc, "Deklaratë Origjinaliteti", 14)
shto_tekst(doc, "Unë, Blerina Tafaj, deklaroj se ky punim diplome është rezultat i punës sime origjinale kërkimore dhe se çdo burim, ide apo material i marrë nga punime të tjera është cituar dhe referuar sipas rregullave akademike në fuqi. Ky punim nuk është paraqitur më parë për vlerësim në asnjë institucion tjetër arsimor.\n\nTiranë, [data], 2026\nNënshkrimi: ____________________")

# --- FALËNDERIME ---
doc.add_page_break()
shto_titull_qender(doc, "Falënderime", 14)
shto_tekst(doc, "[Shto këtu falënderime për udhëheqësen/udhëheqësin shkencor, familjen, kolegët, ose institucionin — zakonisht 1 paragraf, opsionale por e rekomandueshme]")

# --- ABSTRAKT (SHQIP) ---
doc.add_page_break()
shto_titull_qender(doc, "Abstrakt", 14)
shto_tekst(doc, "Ky punim trajton problematikën e zbulimit automatik të të dhënave personale identifikuese (Personally Identifiable Information – PII) në tekste, duke përdorur një model të bazuar në arkitekturën Transformer, konkretisht RoBERTa. Për shkak të mungesës së korpuseve të etiketuara në gjuhën shqipe, modeli u trajnua mbi një dataset standard ndërkombëtar (në anglisht) për të vlerësuar aftësinë e tij gjeneralizuese (transfer learning) dhe qëndrueshmërinë përballë të dhënave jashtë shpërndarjes fillestare (out-of-distribution data), siç janë inputet lokale shqiptare.")
shto_tekst(doc, "Në kuadër të punimit trajtohet evoluimi historik i metodave të Njohjes së Entiteteve me Emër (Named Entity Recognition – NER), duke krahasuar qasjet klasike (Regular Expressions, Hidden Markov Models, Conditional Random Fields) me qasjet moderne kontekstuale. Argumentohet dhe justifikohet inxhinierikisht vendimi për të mos përdorur teknika si Stemming, Lemmatization apo heqjen e Stop Words, pasi këto praktika cenojnë kontekstin që modelet Transformer e shfrytëzojnë për saktësi më të lartë.")
shto_tekst(doc, "Modeli u trajnua duke përdorur skemën BIO (B-/I-/O) të etiketimit. Performanca u mat përmes metrikave Precision, Recall dhe F1-Score, dhe u analizuan thellësisht rastet e gabimeve për të kuptuar kufizimet e modelit kur përballet me toponime apo struktura të panjohura lokale. Rezultatet tregojnë se qasja e bazuar në RoBERTa arrin nivele të larta saktësie për entitetet universale, duke konfirmuar hipotezën fillestare. Në përfundim, u zhvillua një aplikacion Web demonstrues me Streamlit, që lejon testimin interaktiv të modelit.")
shto_tekst(doc, "Fjalë kyçe: PII, RoBERTa, Transfer Learning, NER, Transformer, Machine Learning, Siguria e të Dhënave")

# --- ABSTRACT (ENGLISH) ---
doc.add_page_break()
shto_titull_qender(doc, "Abstract", 14)
shto_tekst(doc, "This thesis addresses the automatic detection of Personally Identifiable Information (PII) using a Transformer-based architecture, specifically RoBERTa. Due to the lack of labeled corpora in the Albanian language, the model was trained on a standard international dataset (in English) to evaluate its generalization ability (transfer learning) and robustness against out-of-distribution data, such as local Albanian inputs.")
shto_tekst(doc, "The work reviews the evolution of Named Entity Recognition (NER) methods, comparing classical approaches (Regular Expressions, Hidden Markov Models, Conditional Random Fields) with modern contextual approaches. It justifies the engineering decision to avoid Stemming, Lemmatization, and Stop Word removal, since these practices compromise the context that Transformer models rely on for higher accuracy.")
shto_tekst(doc, "The model was trained using a BIO-labeled dataset. Performance was measured using Precision, Recall, and F1-Score, with an in-depth error analysis to identify the model's limitations when facing unknown local toponyms or structures. Results confirm the initial hypothesis for universal entities, and a demonstrative Streamlit web application was developed to allow interactive testing of the model.")
shto_tekst(doc, "Keywords: PII, RoBERTa, Transfer Learning, NLP, NER, Transformer, Machine Learning, Data Security")

# --- TABELA E PËRMBAJTJES ---
doc.add_page_break()
shto_titull_qender(doc, "Tabela e Përmbajtjes", 14)
doc.add_paragraph()
shto_rresht_toc(doc, "Kapitulli 1: Hyrje", "1", bold=True)
shto_rresht_toc(doc, "1.1 Konteksti i Kërkimit dhe Rëndësia e Temës", "1", indent=0.3)
shto_rresht_toc(doc, "1.2 Formulimi i Hipotezës", "1", indent=0.3)
shto_rresht_toc(doc, "1.3 Qëllimi dhe Objektivat e Punimit", "2", indent=0.3)
shto_rresht_toc(doc, "1.4 Struktura e Punimit", "2", indent=0.3)
shto_rresht_toc(doc, "Kapitulli 2: Sfondi Teorik dhe Rishikimi i Literaturës", "3", bold=True)
shto_rresht_toc(doc, "2.1 Nxjerrja e Informacionit dhe Sistemet e Hershme", "3", indent=0.3)
shto_rresht_toc(doc, "2.2 Modelet Tradicionale të Machine Learning në NLP", "4", indent=0.3)
shto_rresht_toc(doc, "2.3 Përgatitja e Tekstit në Modelet Klasike (Sfidat)", "5", indent=0.3)
shto_rresht_toc(doc, "2.3.1 Lemmatization dhe Stemming", "5", indent=0.6)
shto_rresht_toc(doc, "2.3.2 Menaxhimi i Stop Words", "6", indent=0.6)
shto_rresht_toc(doc, "2.4 Evolucioni drejt Modeleve Kontekstuale dhe Arkitektura Transformer", "7", indent=0.3)
shto_rresht_toc(doc, "Kapitulli 3: Metodologjia dhe Përgatitja e të Dhënave", "9", bold=True)
shto_rresht_toc(doc, "3.1 Analiza dhe Burimi i të Dhënave (Dataset-i Anglisht)", "9", indent=0.3)
shto_rresht_toc(doc, "3.2 Pastrimi dhe Formatimi i të Dhënave (Data Cleaning)", "10", indent=0.3)
shto_rresht_toc(doc, "3.3 Qasja e Re ndaj Stop Words dhe Lematizimit", "11", indent=0.3)
shto_rresht_toc(doc, "3.4 Tokenizimi i Avancuar me Byte-Pair Encoding", "12", indent=0.3)
shto_rresht_toc(doc, "3.5 Mjedisi i Zhvillimit dhe Infrastruktura", "13", indent=0.3)
shto_rresht_toc(doc, "Kapitulli 4: Implementimi Eksperimental", "14", bold=True)
shto_rresht_toc(doc, "4.1 Trajnimi i Modelit për Klasifikimin e Entiteteve", "14", indent=0.3)
shto_rresht_toc(doc, "4.2 Ndërtimi i Arkitekturës së Aplikacionit (Web UI)", "16", indent=0.3)
shto_rresht_toc(doc, "4.3 Logjika e Përkthimit të Etiketave", "17", indent=0.3)
shto_rresht_toc(doc, "Kapitulli 5: Analiza e Rezultateve dhe Diskutimi", "19", bold=True)
shto_rresht_toc(doc, "5.1 Metrikat e Vlerësimit të Saktësisë", "19", indent=0.3)
shto_rresht_toc(doc, "5.2 Analiza e Performancës Sasiore", "20", indent=0.3)
shto_rresht_toc(doc, "5.3 Matrica e Ngatërresave (Confusion Matrix)", "22", indent=0.3)
shto_rresht_toc(doc, "5.4 Sfidat me të Dhënat Lokale (Error Analysis mbi toponimet shqiptare)", "23", indent=0.3)
shto_rresht_toc(doc, "Kapitulli 6: Konkluzione dhe Rekomandime për Punë të Mëtejshme", "25", bold=True)
shto_rresht_toc(doc, "6.1 Përmbledhje e Kontributeve Kryesore", "25", indent=0.3)
shto_rresht_toc(doc, "6.2 Kufizimet e Studimit", "26", indent=0.3)
shto_rresht_toc(doc, "6.3 Rekomandime për Punë të Mëtejshme", "26", indent=0.3)
shto_rresht_toc(doc, "Bibliografia / Referencat", "28", bold=True)
shto_rresht_toc(doc, "Shtojca", "30", bold=True)

# --- LISTAT ---
doc.add_page_break()
shto_titull_qender(doc, "Lista e Figurave dhe Tabelave", 14)
shto_tekst(doc, "[Kjo listë gjenerohet automatikisht në Word: References → Insert Table of Figures]")

doc.add_page_break()
shto_titull_qender(doc, "Lista e Shkurtimeve", 14)
shto_tekst(doc, "•    PII — Personally Identifiable Information\n•    NLP — Natural Language Processing\n•    NER — Named Entity Recognition\n•    HMM — Hidden Markov Model\n•    CRF — Conditional Random Field\n•    BPE — Byte-Pair Encoding\n•    BIO — Beginning-Inside-Outside\n•    GPU — Graphics Processing Unit\n•    UI — User Interface")

# --- KAPITULLI 1 ---
shto_titull_kapitulli(doc, "Kapitulli 1: Hyrje")
shto_nen_titull(doc, "1.1 Konteksti i Kërkimit dhe Rëndësia e Temës")
shto_tekst(doc, "Në këtë nënkapitull trajtohet pse mbrojtja e të dhënave personale (PII) është kthyer në një çështje kritike në epokën e transformimit digjital. Zbulimi i tyre në kohë reale kërkon sisteme inteligjente, veçanërisht kur përballemi me gjuhë që nuk kanë burime të mëdha të dhënash të gatshme.")

shto_nen_titull(doc, "1.2 Formulimi i Hipotezës")
shto_tekst(doc, "Hipoteza kryesore: Modelet e bazuara në arkitekturën Transformer (RoBERTa) mund të përgjithësojnë dhe transferojnë njohuritë e tyre nga dataset-e standarde ndërkombëtare për të identifikuar entitete universale PII, pa pasur nevojë për teknika tradicionale të thjeshtimit sintaksor të tekstit.")

shto_nen_titull(doc, "1.3 Qëllimi dhe Objektivat e Punimit")
shto_tekst(doc, "Qëllimi është ndërtimi i një sistemi PII me RoBERTa dhe vlerësimi i tij. Objektivat: (i) përgatitja e formatit JSON për stërvitje; (ii) optimizimi i modelit për Token Classification; (iii) vlerësimi se si modeli sillet me tekste të reja jashtë dataset-it origjinal; (iv) zhvillimi i Web UI.")

shto_nen_titull(doc, "1.4 Struktura e Punimit")
shto_tekst(doc, "Kapitulli 2 shtjellon teorinë e modeleve NLP. Kapitulli 3 përshkruan metodologjinë dhe natyrën e të dhënave të përdorura. Kapitulli 4 demonstron implementimin praktik. Kapitulli 5 analizon gabimet, veçanërisht kufizimet me toponimet shqiptare. Kapitulli 6 jep përfundimet.")

# --- KAPITULLI 2 ---
shto_titull_kapitulli(doc, "Kapitulli 2: Sfondi Teorik dhe Rishikimi i Literaturës")
shto_nen_titull(doc, "2.1 Nxjerrja e Informacionit dhe Sistemet e Hershme")
shto_tekst(doc, "Përdorimi i Regular Expressions (RegEx) ofronte zgjidhje për formate fikse, por dështonte në njohjen e entiteteve komplekse ose fjalive të paorganizuara.")

shto_nen_titull(doc, "2.2 Modelet Tradicionale të Machine Learning në NLP")
shto_tekst(doc, "Modele si HMM dhe CRF ofruan qasje probabilistike, por vuanin nga paaftësia për të ruajtur kontekstin e gjatë brenda një fjalie të përbërë.")

shto_nen_titull(doc, "2.3 Përgatitja e Tekstit në Modelet Klasike (Sfidat)")
shto_nen_titull(doc, "2.3.1 Lemmatization dhe Stemming", 3)
shto_tekst(doc, "Këto procese reduktonin fjalët në rrënjën e tyre për të ulur ngarkesën kompjuterike të modeleve të vjetra, por shkatërronin informacionin gramatikor.")

shto_nen_titull(doc, "2.3.2 Menaxhimi i Stop Words", 3)
shto_tekst(doc, "Heqja e fjalëve lidhëse removes context. Në modelet klasike kjo ishte domosdoshmëri, por për modelet moderne kjo praktikë është e dëmshme.")

shto_nen_titull(doc, "2.4 Evolucioni drejt Modeleve Kontekstuale dhe Arkitektura Transformer")
shto_tekst(doc, "Arkitektura Transformer, nëpërmjet mekanizmit Self-Attention, mundësoi leximin e fjalisë si një e tërë, duke e bërë fshirjen e stop words totalisht të panevojshme.")

# --- KAPITULLI 3 ---
shto_titull_kapitulli(doc, "Kapitulli 3: Metodologjia dhe Përgatitja e të Dhënave")
shto_nen_titull(doc, "3.1 Analiza dhe Burimi i të Dhënave (Dataset-i Anglisht)")
shto_tekst(doc, "Për shkak të mungesës së korpuseve specifike PII në gjuhën shqipe, për stërvitjen e modelit u përdor një dataset standard ndërkombëtar (anglisht). Kjo zgjedhje lejon testimin e konceptit të 'Transfer Learning'—aftësisë së modelit për të mësuar koncepte universale dhe për t'i aplikuar ato në gjuhë dhe kontekste të reja.")

shto_nen_titull(doc, "3.2 Pastrimi dhe Formatimi i të Dhënave (Data Cleaning)")
shto_tekst(doc, "Të dhënat u kaluan në format JSON dhe u strukturuan me etiketat B-EMËR, I-TELEFON, etj., duke garantuar një skemë BIO të pastër.")

shto_nen_titull(doc, "3.3 Qasja e Re ndaj Stop Words dhe Lematizimit")
shto_tekst(doc, "Një vendim thelbësor inxhinierik ishte mosaplikimi i asnjë thjeshtimi sintaksor. Fjalët u ruajtën ashtu siç ishin për të mbajtur strukturën natyrale.")

shto_nen_titull(doc, "3.4 Tokenizimi i Avancuar me Byte-Pair Encoding")
shto_tekst(doc, "Tokenizuesi BPE lejon trajtimin e fjalëve të panjohura (si emrat lokalë shqiptarë) duke i copëtuar ato në nën-njësi të njohura.")

shto_nen_titull(doc, "3.5 Mjedisi i Zhvillimit dhe Infrastruktura")
shto_tekst(doc, "U përdor Google Colab me GPU T4 për trajnimin intensiv prej 5 epokash.")

# --- KAPITULLI 4 ---
shto_titull_kapitulli(doc, "Kapitulli 4: Implementimi Eksperimental")
shto_nen_titull(doc, "4.1 Trajnimi i Modelit për Klasifikimin e Entiteteve")
shto_tekst(doc, "Procesi u konfirmua me parametrat e optimizuar (Weight Decay) për të shmangur overfitting mbi dataset-in anglisht.")

shto_nen_titull(doc, "4.2 Ndërtimi i Arkitekturës së Aplikacionit (Web UI)")
shto_tekst(doc, "Integrimi i modelit të gjeneruar në një ndërfaqe Python (Streamlit) për të testuar inputet live nga përdoruesi.")

shto_nen_titull(doc, "4.3 Logjika e Përkthimit të Etiketave")
shto_tekst(doc, "Mekanizmi që përkthen kodet vizuale të Transformerit në një ndërfaqe të lexueshme me theksime ngjyrash.")

# --- KAPITULLI 5 ---
shto_titull_kapitulli(doc, "Kapitulli 5: Analiza e Rezultateve dhe Diskutimi")
shto_nen_titull(doc, "5.1 Metrikat e Vlerësimit të Saktësisë")
shto_tekst(doc, "Analiza e Precision, Recall dhe F1-Score mbi të dhënat e testimit.")

shto_nen_titull(doc, "5.2 Analiza e Performancës Sasiore")
shto_tekst(doc, "Modeli shfaqi saktësi jashtëzakonisht të lartë për entitete me strukturë universale, si numrat e telefonit apo formatet e email-it.")

shto_nen_titull(doc, "5.3 Matrica e Ngatërresave (Confusion Matrix)")
shto_tekst(doc, "Grafiku vizual tregon saktësisht se ku përqendrohen gabimet kryesore gjatë klasifikimit.")

shto_nen_titull(doc, "5.4 Sfidat me të Dhënat Lokale (Error Analysis mbi toponimet shqiptare)")
shto_tekst(doc, "Seksioni më i rëndësishëm analitik: Fakti që modeli u stërvit me dataset anglisht shkakton atë që njihet si sfidë me të dhënat 'Out-of-Distribution'. Për shembull, termi 'Kavajë' u keq-klasifikua nga modeli pasi nuk i përgjigjet strukturave të adresuara gjeografike anglisht, duke theksuar nevojën për fine-tuning shtesë me korpuse shqip.")

# --- KAPITULLI 6 ---
shto_titull_kapitulli(doc, "Kapitulli 6: Konkluzione dhe Rekomandime për Punë të Mëtejshme")
shto_nen_titull(doc, "6.1 Përmbledhje e Kontributeve Kryesore")
shto_tekst(doc, "Projekti demonstroi suksesin e aplikimit të arkitekturave moderne në identifikimin e PII pa humbur kontekstin gjuhësor.")

shto_nen_titull(doc, "6.2 Kufizimet e Studimit")
shto_tekst(doc, "Kufizimi parësor mbetet mungesa e të dhënave sasiore në gjuhën shqipe gjatë fazës së stërvitjes.")

shto_nen_titull(doc, "6.3 Rekomandime për Punë të Mëtejshme")
shto_tekst(doc, "Ndërtimi i një dataset-i masiv PII me adresa dhe toponime nga Shqipëria për të kryer një trajnim të thelluar të versionit multilingual XLM-RoBERTa.")

# --- BIBLIOGRAFIA DHE SHTOJCA ---
shto_titull_kapitulli(doc, "Bibliografia / Referencat")
shto_tekst(doc, "[Këtu shtohen referencat standarde (Vaswani, Liu, Devlin)]")

shto_titull_kapitulli(doc, "Shtojca")
shto_nen_titull(doc, "Shtojca A: Kodi Burimor")
shto_tekst(doc, "[Fragmente të app.py]")

doc.save('Draft2.docx')
print("Skedari u gjenerua: Draft2.docx")