import os



from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_google_community import BigQueryVectorStore

from dotenv import load_dotenv

load_dotenv()

embedding = GoogleGenerativeAIEmbeddings(model="text-embedding-004")

PROJECT_ID = os.getenv("PROJECT")
REGION = os.getenv("REGION")
DATASET= os.getenv("DATASET")
TABLE = os.getenv("TABLE")

vector_store = BigQueryVectorStore(
    project_id=PROJECT_ID,
    dataset_name=DATASET,
    table_name=TABLE,
    location=REGION,
    embedding=embedding,
)

search = vector_store.similarity_search("Security")
print(f"here are the docs searched {search}")