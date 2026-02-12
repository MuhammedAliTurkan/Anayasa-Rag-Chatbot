import streamlit as st
from pypdf import PdfReader

from rag import split_by_madde, build_bm25, retrieve
from llm import ask_llm

st.set_page_config(
    page_title="Anayasa RAG Chatbot",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ Anayasa RAG Chatbot (PDF + RAG)")
st.caption("PDF yükle → maddelere böl → soru sor → cevap + kaynak göster")

# -------------------------
# Session State (NOT: items anahtarını kullanmıyoruz)
# -------------------------
if "docs" not in st.session_state:
    st.session_state["docs"] = None

if "bm25" not in st.session_state:
    st.session_state["bm25"] = None

if "chat" not in st.session_state:
    st.session_state["chat"] = []

# -------------------------
# PDF → TEXT
# -------------------------
def pdf_to_text(file) -> str:
    reader = PdfReader(file)
    pages_text = []
    for page in reader.pages:
        t = page.extract_text()
        if t:
            pages_text.append(t)
    return "\n".join(pages_text)

# -------------------------
# SIDEBAR
# -------------------------
with st.sidebar:
    st.header("PDF Yükle")

    pdf_file = st.file_uploader("Anayasa PDF", type=["pdf"])
    k = st.slider("Retrieve top-k", 1, 5, 3)
    show_sources = st.checkbox("Kaynak parçaları göster", value=True)

    build_button = st.button(
        "PDF'yi İndeksle",
        type="primary",
        disabled=(pdf_file is None)
    )

# -------------------------
# INDEX BUILD
# -------------------------
if build_button:
    with st.spinner("PDF okunuyor..."):
        full_text = pdf_to_text(pdf_file)

    if not full_text or len(full_text.strip()) < 800:
        st.error("PDF'den yeterli metin okunamadı. (PDF taranmış olabilir)")
    else:
        with st.spinner("Maddelere ayrılıyor..."):
            docs = split_by_madde(full_text)  # liste döner

        with st.spinner("BM25 indeks oluşturuluyor..."):
            bm25 = build_bm25(docs)

        st.session_state["docs"] = docs
        st.session_state["bm25"] = bm25
        st.session_state["chat"] = []

        st.success(f"İndekslendi ✅ Parça sayısı: {len(docs)}")

# -------------------------
# CHAT SECTION
# -------------------------
st.divider()

if st.session_state["bm25"] is None:
    st.info("Başlamak için soldan PDF yükleyip 'PDF'yi İndeksle'ye bas.")
else:
    question = st.text_input("Sorun (örnek: 'Bütçe teklifini kim sunar?')")

    ask_button = st.button("💬 Soruyu Cevapla", disabled=(not question.strip()))

    if ask_button:
        docs = st.session_state["docs"]     # <-- dikkat: köşeli parantez
        bm25 = st.session_state["bm25"]

        hits = retrieve(docs, bm25, question, k=k)
        source_texts = [h["text"] for h in hits]

        with st.spinner("Cevap hazırlanıyor..."):
            answer = ask_llm(question, source_texts)

        st.session_state["chat"].append({
            "question": question,
            "answer": answer,
            "hits": hits
        })

# -------------------------
# CHAT HISTORY
# -------------------------
for message in reversed(st.session_state["chat"]):
    with st.container(border=True):
        st.markdown(f"**Soru:** {message['question']}")
        st.markdown(f"**Cevap:** {message['answer']}")

        if show_sources:
            st.markdown("**Kaynaklar (retrieved):**")
            for hit in message["hits"]:
                title = hit.get("title", hit["id"])
                score = hit.get("score", 0.0)
                with st.expander(f"{title} (score={score:.2f})"):
                    st.write(hit["text"])
