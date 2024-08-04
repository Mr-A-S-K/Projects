import os
import streamlit as st
from langchain_community.llms import GooglePalm
from langchain.prompts import PromptTemplate
import cohere
from transformers import pipeline
from API_KEY import COHERE_API_KEY, GOOGLE_API_KEY

# Ensure the environment variables are set, or set them directly here for testing purposes
os.environ['COHERE_API_KEY'] = COHERE_API_KEY
os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY

# Initialize Cohere client
co = cohere.Client(api_key=os.environ.get('COHERE_API_KEY'))

COHERE_EMBEDDING_MODEL = 'embed-english-v3.0'

def fetch_embeddings(texts: list[str], embedding_type: str = 'search_document') -> list[list[float]]:
    try:
        results = co.embed(
            texts=texts,
            model=COHERE_EMBEDDING_MODEL,
            input_type=embedding_type
        ).embeddings
        return results
    except Exception as e:
        st.error(f'Cohere embedding fetch failed with error: {e}')
        return []

def get_llm_model(model_name: str):
    if model_name == 'Google PaLM':
        return GooglePalm(api_key=os.environ.get('GOOGLE_API_KEY'))
    elif model_name == 'BERT':
        return pipeline("question-answering", model="deepset/bert-base-cased-squad2")
    elif model_name == 'GPT-2':
        return pipeline("text-generation", model="gpt2")
    else:
        raise ValueError(f"Model {model_name} is not supported.")

def synthesize_answer(model_name: str, question: str, context: list[str]) -> str:
    context_str = '\n'.join(context)
    prompt = question_and_answer_prompt(question, context)
    
    if model_name == 'Google PaLM':
        llm = get_llm_model(model_name)
        response = llm.generate([prompt])  # Pass a list of strings
        return response.generations[0][0].text  # Access the first generation's text
    else:
        qa_pipeline = get_llm_model(model_name)
        if model_name == 'BERT':
            response = qa_pipeline(question=question, context=context_str)
            return response['answer']
        elif model_name == 'GPT-2':
            response = qa_pipeline(prompt, max_length=150)
            return response[0]['generated_text']

def question_and_answer_prompt(question: str, context: list[str]) -> str:
    context_str = '\n'.join(context)
    return f"""
    Context information is below.
    ---------------------
    {context_str}
    ---------------------
    Given the context information and not prior knowledge, answer the query.
    Query: {question}
    Answer: 
    """

# Streamlit UI
st.title("Document Reader and Q&A with LLMs")

# File upload
uploaded_file = st.file_uploader("Upload a document", type=["pdf", "docx", "txt"])
texts = []

if uploaded_file:
    file_extension = uploaded_file.name.split('.')[-1].lower()
    if file_extension in ['pdf']:
        import fitz  # PyMuPDF
        doc = fitz.open(stream=uploaded_file.read(), filetype='pdf')
        texts = [page.get_text() for page in doc]
    elif file_extension in ['docx']:
        import docx
        doc = docx.Document(uploaded_file)
        texts = [para.text for para in doc.paragraphs]
    elif file_extension in ['txt']:
        texts = uploaded_file.read().decode('utf-8').splitlines()

# Display uploaded content
if texts:
    st.subheader("Document Content")
    st.write('\n'.join(texts))

# Embeddings
if texts:
    if st.button("Fetch Embeddings"):
        embeddings = fetch_embeddings(texts)
        if embeddings:
            st.success("Embeddings fetched successfully!")

# Question and Answer
if texts:
    st.subheader("Question and Answer")
    question = st.text_input("Enter your question:")
    model_name = st.selectbox("Select an LLM:", ["Google PaLM", "BERT", "GPT-2"])

    if st.button("Get Answer"):
        if question and model_name:
            answer = synthesize_answer(model_name, question, texts)
            st.write("Answer:", answer)
        else:
            st.error("Please provide a question and select an LLM.")
