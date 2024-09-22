# Document QA Bot

This is a Streamlit application that creates an interactive chatbot capable of answering questions about uploaded documents. It uses Groq for language model inference, Pinecone for vector storage and retrieval, and SentenceTransformer for text embedding.

## Features

- Document processing (PDF, DOCX, TXT, MD)
- Text indexing and retrieval
- Question answering based on document content
- Interactive chat interface

## Prerequisites

Before you begin, ensure you have the following:

- Python 3.7 or higher
- Groq API key
- Pinecone API key

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/marvlyngkhoi/RAG_CHATBOT.git
   cd document-qa-bot
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

   Note: You may need to create a `requirements.txt` file with the following content:

   ```
   streamlit
   groq
   pinecone-client
   sentence-transformers
   PyPDF2
   python-docx
   textract
   ```

## Usage

1. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

2. Open your web browser and go to the URL provided by Streamlit (usually `http://localhost:8501`).

3. In the sidebar, enter your Groq API key, Pinecone API key, and vector index database name.

4. Click "Initialize" to set up the application.

5. Upload a document using the file uploader.

6. Click "Process Document" to index the document.

7. Ask questions in the chat interface and receive answers based on the document content.

## Configuration

You can adjust the following parameters in the sidebar:

- Number of top results to retrieve (default: 3)
- Vector Index Database Name (default: "rag-doc")

## Customization

- To change the language model, modify the `model` parameter in the `groq_client.chat.completions.create()` function.
- To use a different embedding model, change the model name in `SentenceTransformer('all-MiniLM-L6-v2')`.

## Troubleshooting

- If you encounter issues with PDF processing, ensure you have the necessary system dependencies for PyPDF2.
- For problems with DOCX files, check that python-docx is correctly installed.
- If you face issues with other file types, make sure textract and its dependencies are properly set up.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

