import os

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_google_community import BigQueryVectorStore
from dotenv import load_dotenv

load_dotenv()

# Embedding model (Gemini embeddings via API key)
embedding = GoogleGenerativeAIEmbeddings(model="text-embedding-004")

"""
List of URLs for the certification knowledge base. This includes the study guides for the most popular cloud certifications:
1. Google Cloud Associate Cloud Engineer
2. Google Cloud Professional Cloud Security Engineer
"""

urls = [
    "https://services.google.com/fh/files/misc/associate_cloud_engineer_exam_guide_english.pdf",
    "https://services.google.com/fh/files/misc/professional_cloud_security_engineer_exam_guide_english.pdf",
]

# Load the documents and split them into chunks
loader = UnstructuredURLLoader(urls)
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
texts = text_splitter.split_documents(documents)

for idx, split in enumerate(texts):
    split.metadata["chunk"] = idx

# Creating the Vector store in BigQuery
vector_store = BigQueryVectorStore(
    project_id=os.getenv("PROJECT"),
    dataset_name=os.getenv("DATASET"),
    table_name=os.getenv("TABLE"),
    location=os.getenv("REGION"),
    embedding=embedding,
)

# Add the documents to the vector store
vector_store.add_documents(texts)
