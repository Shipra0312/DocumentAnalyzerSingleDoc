import os
import streamlit as st
import openai
from PyPDF2 import PdfReader

# Fetch the OpenAI API key
openai.api_key = st.secrets["openai_api_key"]

def extract_text_from_pdf(file):
    """Extract text from a PDF file."""
    reader = PdfReader(file)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

def query_gpt4(prompt):
    """Query the GPT-4 model and return the response."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def main():
    """Main function to run the Streamlit app."""
    st.title("PDF Document Analyzer")

    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
    if uploaded_file is not None:
        text = extract_text_from_pdf(uploaded_file)
        st.text_area("Extracted Text", text, height=250)

        st.subheader("Ask Questions About the Document")
        
        # Use a session state to keep track of questions and answers
        if 'questions' not in st.session_state:
            st.session_state.questions = []
        
        # Input for new question
        question = st.text_input("Type your question here:")
        
        # Button to submit the question
        if st.button("Ask"):
            if question:
                st.session_state.questions.append(question)
                full_prompt = f"Based on the following document: {text}\n\nAnswer the question: {question}"
                answer = query_gpt4(full_prompt)
                st.session_state.questions.append(answer)

        # Display all questions and answers
        if st.session_state.questions:
            for i in range(0, len(st.session_state.questions), 2):
                st.write(f"**Question {i//2 + 1}:** {st.session_state.questions[i]}")
                st.write(f"**Answer:** {st.session_state.questions[i+1]}")

if __name__ == "__main__":
    main()
