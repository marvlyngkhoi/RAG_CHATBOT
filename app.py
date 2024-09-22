import time
import streamlit as st
import os
import groq
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
from typing import List, Dict
import PyPDF2
from docx import Document
import textract
from functools import lru_cache

# Streamlit configurations
st.set_page_config(page_title="Document QA Bot", page_icon="📚", layout="wide")
st.title("Document QA Bot")

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = False
    st.session_state.data_chunks = []
    st.session_state.chat_history = []
    st.session_state.retrieved_chunks = {}

# Sidebar for API keys and initialization
with st.sidebar:
    st.header("Configuration")
    groq_api_key = st.text_input("Enter Groq API Key", type="password")
    pinecone_api_key = st.text_input("Enter Pinecone API Key", type="password")
    vector_index_name = st.text_input("Enter Vector Index Database Name")
    top_k = st.slider("Number of top results to retrieve", min_value=1, max_value=10, value=3)
    
    if st.button("Initialize"):
        # Set up Groq API
        groq_client = groq.Groq(api_key=groq_api_key)
        
        # Set up Pinecone
        pc = Pinecone(api_key=pinecone_api_key)
        index_name = vector_index_name if vector_index_name else "rag-doc"
        
        # Load Sentence Transformer model
        model = SentenceTransformer('all-MiniLM-L6-v2')
        cloud = 'aws'
        region = 'us-east-1'
        spec = ServerlessSpec(cloud=cloud, region=region)
        
        # Create Pinecone index if it doesn't exist
        if index_name not in pc.list_indexes().names():
            pc.create_index(
                name=index_name,
                dimension=384,
                metric="cosine",
                spec=spec
            )
            while not pc.describe_index(index_name).status['ready']:
                time.sleep(1)
        
        st.session_state.initialized = True
        st.session_state.groq_client = groq_client
        st.session_state.index = pc.Index(index_name)
        st.session_state.model = model
        st.success("Initialization complete!")

# Functions for text extraction and processing
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(file):
    doc = Document(file)
    return "\n".join([paragraph.text for paragraph in doc.paragraphs])

def extract_text_from_file(file):
    file_extension = os.path.splitext(file.name)[1].lower()
    if file_extension == '.pdf':
        return extract_text_from_pdf(file)
    elif file_extension == '.docx':
        return extract_text_from_docx(file)
    elif file_extension in ['.txt', '.md']:
        return file.getvalue().decode('utf-8')
    else:
        # For other file types, use textract
        return textract.process(file.read()).decode('utf-8')

def load_data(file) -> List[str]:
    text = extract_text_from_file(file)
    chunks = text.split('\n\n')
    return [chunk.strip() for chunk in chunks if chunk.strip()]

@lru_cache(maxsize=1000)
def get_embedding(text: str) -> List[float]:
    return st.session_state.model.encode(text).tolist()

def index_data(chunks: List[str]):
    vectors = []
    for i, chunk in enumerate(chunks):
        embedding = get_embedding(chunk)
        vectors.append((str(i), embedding, {"text": chunk}))
    st.session_state.index.upsert(vectors=vectors)

@lru_cache(maxsize=100)
def retrieve_relevant_chunks(query: str, top_k: int) -> List[Dict]:
    query_embedding = get_embedding(query)
    results = st.session_state.index.query(vector=query_embedding, top_k=top_k, include_metadata=True)
    return results['matches']

@lru_cache(maxsize=100)
def generate_answer(query: str, context: str) -> str:
    prompt = f"Context:\n{context}\n\nQuestion: {query}\n\nAnswer:"
    
    response = st.session_state.groq_client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that answers questions based on the given context."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.7,
    )
    
    return response.choices[0].message.content.strip()

# Main application
if st.session_state.initialized:
    uploaded_file = st.file_uploader("Choose a document", type=['pdf', 'docx', 'txt', 'md'])
    
    if uploaded_file is not None:
        if st.button("Process Document"):
            with st.spinner("Processing document..."):
                st.session_state.data_chunks = load_data(uploaded_file)
                index_data(st.session_state.data_chunks)
            st.success("Document processed and indexed successfully!")
    
    # Chat interface and content display
    st.header("Chat with your document")
    
    # Create two columns
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("Chat")
        
        # Use an empty container for the chat history
        chat_container = st.empty()
        
        # User input
        user_question = st.text_input("Ask a question about your document:")
        
        if user_question:
            with st.spinner("Generating answer..."):
                relevant_chunks = retrieve_relevant_chunks(user_question, top_k)
                context = "\n".join([chunk['metadata']['text'] for chunk in relevant_chunks])
                answer = generate_answer(user_question, context)
            
            st.session_state.chat_history.append(("You", user_question))
            st.session_state.chat_history.append(("Bot", answer))
            st.session_state.retrieved_chunks[user_question] = relevant_chunks
        
        # Display chat history with highlighted questions
        chat_content = ""
        for role, message in st.session_state.chat_history:
            if role == "You":
                chat_content += f"**You:** :blue[{message}]\n\n"
            else:
                chat_content += f"Bot: {message}\n\n"
        chat_container.markdown(chat_content)
    
    with col2:
        st.subheader("Retrieved Content")
        # Display retrieved content for the last question
        if st.session_state.chat_history:
            last_question = st.session_state.chat_history[-2][1]  # Get the last user question
            if last_question in st.session_state.retrieved_chunks:
                st.write(f"Retrieved content for: '{last_question}'")
                for i, chunk in enumerate(st.session_state.retrieved_chunks[last_question]):
                    with st.expander(f"Chunk {i+1} (Score: {chunk['score']:.4f})"):
                        st.write(chunk['metadata']['text'])

else:
    st.warning("Please initialize the application with your API keys in the sidebar.")

# Run the Streamlit app
if __name__ == "__main__":
    # The Streamlit CLI command to run this:
    # streamlit run this_script.py
    pass