# Import necessary libraries
import os
import streamlit as st
from pathlib import Path
import pytesseract
import pdfplumber
from PIL import Image
import openai

# Set your OpenAI API key
openai.api_key = 'your-api-key'

# Preprocess the document to ensure it is in a machine-readable format
def preprocess_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

def preprocess_image(file_path):
    image = Image.open(file_path)
    text = pytesseract.image_to_string(image)
    return text

def call_open_ai(text, maxtokens):
    response = openai.Completion.create(
        engine="text-davinci-003", 
        prompt=text,
        max_tokens=maxtokens,
        n=1,
        stop=None,
        temperature=0.5
    )
    extracted_info = response.choices[0].text.strip()
    return extracted_info

# Extract key financial metrics and information from the statements using LLMs
def extract_information(document):
    prompt = f"Extract the key metrics from the document:\n{document}"
    extracted_info = call_open_ai(prompt, 500)
    return extracted_info

# Check compliance using the OpenAI API
def check_compliance(extracted_info):
    prompt = f"Analyse the metrics from the document:\n{extracted_info}"
    compliance_results = call_open_ai(prompt, 500)
    return compliance_results

# Generate a summary of the financial statements using the OpenAI API
def generate_summary(extracted_info):
    prompt = f"Summarize the information from the document:\n{extracted_info}"
    summary = call_open_ai(extracted_info)
    return summary


# Define Streamlit app
def main():
    st.title("Automated Financial Statement Analysis and Compliance Check")
    st.write("Upload your financial statements to analyze and check for compliance.")

    # File upload
    uploaded_file = st.file_uploader("Upload financial statement", type=["pdf", "png", "jpg", "jpeg"])

    if uploaded_file is not None:
        # Preprocessing
        file_path = Path(uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        if file_path.suffix == ".pdf":
            document = preprocess_pdf(file_path)
        else:
            document = preprocess_image(file_path)

        # Information extraction
        extracted_info = extract_information(document)

        # Compliance analysis
        compliance_results = check_compliance(extracted_info)

        # Summarization
        summary = generate_summary(extracted_info, compliance_results)

        # Display results
        st.subheader("Extracted Information")
        st.write(extracted_info)

        st.subheader("Compliance Analysis")
        st.write(compliance_results)

        st.subheader("Summary")
        st.write(summary)

if __name__ == "__main__":
    main()