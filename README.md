# Gemini LangChain RAG

A demo project that builds a **Google Cloud Certifications Chatbot** using **LangChain**, the **Gemini API**, and **BigQuery** as a vector store. The chatbot can answer questions about Google Cloud certifications by retrieving relevant content from official exam guides and generating responses with a Gemini model. [file:1][file:2][file:5][file:6]

## Project Structure

- **`ai.py`**  
  Contains the AI helper function that:
  - Runs similarity search over the BigQuery vector store.  
  - Calls a Gemini chat model (for example `gemini-2.0-flash`) to answer user questions using retrieved document chunks. [file:2][file:5]

- **`knowledge_base.py`**  
  Loads Google Cloud certification PDFs from URLs, splits them into text chunks, creates embeddings with `GoogleGenerativeAIEmbeddings`, and writes them into a BigQuery table via `BigQueryVectorStore`. [file:1][web:7][web:8]

- **`search.py`**  
  Simple script that runs a `similarity_search` query against the BigQuery vector store to verify that documents are stored and searchable. [file:2][web:7]

- **`vertexai_vectorsearch.py`**  
  Alternative example showing how vector search could be implemented with Vertex AI Matching Engine; not required for the main Streamlit demo. [file:4][web:72]

- **`streamlit.py`**  
  Streamlit web app that exposes a chatbot UI for asking questions about Google Cloud certifications and displaying answers. [file:6][web:16]

- **`.env`**  
  Environment configuration file for project settings (GCP project, dataset, table, region, Gemini API key). [file:1][file:5]

- **`requirements.txt`**  
  Python dependencies (LangChain core, Gemini integration, BigQuery vector store, document loaders, Streamlit, etc.). [file:3]

## Prerequisites

- Python **3.9+**. [attached_file:1]  
- A **Google Cloud project** with:
  - Billing enabled. [web:108]
  - **BigQuery API** enabled. [web:7][web:73]
  - **Gemini API** (`generativelanguage.googleapis.com`) enabled. [web:35][web:108]
- Local Google Cloud authentication (Application Default Credentials) for BigQuery:


## Setup

1. **Clone the repository**
git clone https://github.com/rohitkumbhar7009/gemini-langchain-rag.git
cd gemini-langchain-rag


2. **Create and activate a virtual environment**


python -m venv .venv

Windows
..venv\Scripts\activate

Linux / macOS
source .venv/bin/activate


3. **Configure environment variables**

Create a `.env` file in the project root:


PROJECT= # your GCP project ID
DATASET= # BigQuery dataset name
TABLE= # BigQuery table name
REGION= # BigQuery dataset region
GOOGLE_API_KEY= # Gemini API key from Google AI Studio


- `GOOGLE_API_KEY` is created in **Google AI Studio → API keys**. [web:33][web:40][web:42]  
- `PROJECT`, `DATASET`, `TABLE`, `REGION` must match your BigQuery configuration. [web:7][web:73]

4. **Install dependencies**

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

## Running the Demo

### 1. Load the knowledge base

Run `knowledge_base.py` to download the exam guide PDFs, chunk them, create embeddings, and populate the BigQuery vector table. [file:1][web:7][web:8]

python knowledge_base.py
This initializes or updates the table:

PROJECT.DATASET.TABLE -> e.g. gcp-cert-bot.cert_kb.cert_docs


You can confirm rows in the BigQuery console. [web:7][web:73]

### 2. Test vector search

Run a sample similarity search against the vector store. [file:2]


python search.py

If everything is configured correctly, the script prints relevant chunks from the certification exam guides for the sample query (such as `"Security"`). [file:2][file:1]

### 3. Test the AI helper from CLI

`ai.py` exposes an `ai_helper` function that combines BigQuery similarity search with a Gemini chat model. [file:5][web:24]


python ai.py

This invokes `ai_helper` with a sample question (for example “How can I pass Associate Cloud Engineer exam?”) and prints the model’s answer. [file:5]

### 4. Run the Streamlit chatbot

Launch the web UI with Streamlit. [file:6][web:16][web:22]


streamlit run streamlit.py


Then open the local URL shown in the terminal (usually `http://localhost:8501`) and:

- Type any question about Google Cloud certifications in the input box.  
- The app retrieves relevant document chunks from BigQuery and uses the Gemini chat model to generate a response. [file:5][file:6]

## Notes

- BigQuery vector storage is implemented with LangChain’s `BigQueryVectorStore` integration. [file:1][file:2][web:8][web:26]  
- Document splitting uses `CharacterTextSplitter` from `langchain-text-splitters` to create overlapping chunks suitable for retrieval. [file:1][web:56]
- Gemini integration uses `GoogleGenerativeAIEmbeddings` for embeddings and `ChatGoogleGenerativeAI` for chat, both configured via the `GOOGLE_API_KEY` in `.env`. [file:1][file:5][web:21][web:24][web:35]
- If you see quota or API errors from Gemini, check your project’s billing and Gemini rate limits. [web:105][web:110][web:112]

## License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.

## Author

- GitHub: **rohitkumbhar7009**  


