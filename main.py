import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import pandas as pd
import json
import xml.etree.ElementTree as ET
from docx import Document
from PyPDF2 import PdfReader

# Define AIModelFactory and model classes
class AIModelFactory:
    @staticmethod
    def get_model(model_name, credentials):
        if model_name == "gpt2":
            return GPT2Model(credentials)
        elif model_name == "tinyllama":
            return TinyLlamaModel(credentials)
        else:
            raise ValueError(f"Unsupported model: {model_name}")

class GPT2Model:
    def __init__(self, credentials):
        self.tokenizer = AutoTokenizer.from_pretrained("openai-community/gpt2")
        self.model = AutoModelForCausalLM.from_pretrained("openai-community/gpt2")
        self.pipe = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer)

    def generate_text(self, prompt):
        result = self.pipe(prompt, max_length=150, max_new_tokens=50, num_return_sequences=1)
        return result[0]["generated_text"]

class TinyLlamaModel:
    def __init__(self, credentials):
        self.tokenizer = AutoTokenizer.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0")
        self.model = AutoModelForCausalLM.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0")
        self.pipe = pipeline("summarization", model=self.model, tokenizer=self.tokenizer)

    def generate_text(self, prompt):
        result = self.pipe(prompt, max_length=150, max_new_tokens=50, num_return_sequences=1)
        return result[0]["summary_text"]

class DataExtractor:
    def __init__(self, model_name, credentials):
        self.model = AIModelFactory.get_model(model_name, credentials)
    
    def extract_data(self, content):
        return self.model.generate_text(content)

def extract_text_from_file(file):
    if file.type == "application/pdf":
        return extract_text_from_pdf(file)
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return extract_text_from_docx(file)
    elif file.type == "text/csv":
        return extract_text_from_csv(file)
    elif file.type == "text/plain":
        return extract_text_from_txt(file)
    else:
        return "Unsupported file type"

def extract_text_from_pdf(file):
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

def extract_text_from_docx(file):
    doc = Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def extract_text_from_csv(file):
    df = pd.read_csv(file)
    return df.to_string()

def extract_text_from_txt(file):
    return file.read().decode("utf-8")

def text_to_json(text):
    return json.dumps({"content": text}, indent=4)

def text_to_xml(text):
    root = ET.Element("root")
    content = ET.SubElement(root, "content")
    content.text = text
    return ET.tostring(root, encoding="unicode")

# Streamlit UI
st.title("Document Content Extraction")

uploaded_file = st.file_uploader("Upload a document", type=["pdf", "docx", "csv", "txt"])
selected_model = st.selectbox("Select a model", ["gpt2", "tinyllama"])
credentials = {}  # Add your credentials if needed

if st.button("Extract Content"):
    if uploaded_file is not None:
        with st.spinner("Extracting content..."):
            # Extract text from the uploaded file
            text = extract_text_from_file(uploaded_file)

            if not text:
                st.error("No text was extracted from the file.")
            else:
                # Initialize the DataExtractor with the selected model
                data_extractor = DataExtractor(selected_model, credentials)

                try:
                    # Generate text using the model
                    extracted_content = data_extractor.extract_data(text)
                except Exception as e:
                    st.error(f"Error generating text: {e}")
                    extracted_content = "An error occurred during text generation."

                # Convert extracted content to JSON and XML
                json_content = text_to_json(extracted_content)
                xml_content = text_to_xml(extracted_content)

                # Display the results
                st.subheader("Extracted Content")
                st.text_area("Text", extracted_content, height=200)
                st.subheader("JSON")
                st.text_area("JSON", json_content, height=200)
                st.subheader("XML")
                st.text_area("XML", xml_content, height=200)
    else:
        st.warning("Please upload a document.")
