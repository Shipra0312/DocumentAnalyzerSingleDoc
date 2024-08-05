import os
import streamlit as st
import openai
from PyPDF2 import PdfReader

# Fetch the OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

def query_gpt4(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300
    )
    return response.choices[0].message['content'].strip()

def main():
    st.title("PDF Document Analyzer")
    
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
    if uploaded_file is not None:
        text = extract_text_from_pdf(uploaded_file)
        st.text_area("Extracted Text", text, height=250)

        question = st.text_input("Ask a question about the document:")
        if question:
            full_prompt = f"Based on the following document: {text}\n\nAnswer the question: {question}"
            answer = query_gpt4(full_prompt)
            st.write("Answer:", answer)

if __name__ == "__main__":
    main()
