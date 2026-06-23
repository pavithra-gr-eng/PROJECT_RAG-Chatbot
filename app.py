import streamlit as st
import google.generativeai as genai
from pdf_loader import load_and_split_pdf

# Gemini API Key
genai.configure(api_key="GEMINI_API_KEY")

model = genai.GenerativeModel("gemini-2.5-flash")

st.title("RAG Chatbot")

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

pdf_text = ""

if uploaded_file:
    st.success("PDF Uploaded Successfully")

    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())

    chunks = load_and_split_pdf("temp.pdf")

    st.write(f"Number of Chunks: {len(chunks)}")

    pdf_text = "\n".join([chunk.page_content for chunk in chunks])

question = st.text_input("Ask a question about the PDF")

if question and pdf_text:

    prompt = f"""
    Answer only from the PDF content below.

    PDF Content:
    {pdf_text}

    Question:
    {question}
    """

    response = model.generate_content(prompt)

    st.subheader("Answer")
    st.write(response.text)