import os
from google import genai
import PyPDF2
import streamlit as st

# Function to extract text from an uploaded PDF
def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    extracted_text = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            extracted_text += text + "\n"
    return extracted_text

# Function to summarize text using Gemini AI
def summarize_text(text, api_key):
    client = genai.Client(api_key=api_key)
    prompt = f"""
    Summarize the following text clearly using bullet points.
    Highlight the main ideas, key takeaways, and important facts.

    Text content:
    {text[:20000]}
    """
    response = client.models.generate_content(
        model="gemini-3.6-flash", 
        contents=prompt
    )
    return response.text

# Streamlit User Interface
st.set_page_config(page_title="AI PDF Summarizer", layout="centered")
st.title("📄 Simple AI PDF Summarizer")

# Sidebar for Key Input
st.sidebar.header("Setup")
user_api_key = st.sidebar.text_input("Paste Gemini API Key Here:", value="AQ.Ab8RN6L5E7rxy0BuFVWVQlB7rtXgQgo0iAItkLY2CHSb77p94g", type="password")

# File Upload Section
uploaded_file = st.file_uploader("Upload your PDF document", type=["pdf"])

if st.button("Summarize PDF"):
    if not user_api_key:
        st.error("Please enter your Gemini API key in the sidebar.")
    elif not uploaded_file:
        st.warning("Please upload a PDF file first.")
    else:
        with st.spinner("Processing document..."):
            try:
                text = extract_text_from_pdf(uploaded_file)
                if not text.strip():
                    st.error("No text found. PDF might be an image or scan.")
                else:
                    summary = summarize_text(text, user_api_key)
                    st.subheader("📌 Summary")
                    st.write(summary)
            except Exception as e:
                st.error(f"Error: {e}")