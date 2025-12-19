import os

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_google_community import BigQueryVectorStore

load_dotenv()

# Embedding model (Gemini embeddings)
embedding = GoogleGenerativeAIEmbeddings(model="text-embedding-004")

# Vector store (BigQuery)
vector_store = BigQueryVectorStore(
    project_id=os.getenv("PROJECT"),
    dataset_name=os.getenv("DATASET"),
    table_name=os.getenv("TABLE"),
    location=os.getenv("REGION"),
    embedding=embedding,
)


# AI helper function
def ai_helper(query: str):
    # LLM model (Gemini chat)
    llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",  # modern general chat model
    )

    # Retrieve similar documents
    docs = vector_store.similarity_search(query)
    docs_text = " ".join(d.page_content for d in docs)

    # Prompt
    prompt = PromptTemplate(
        input_variables=["question", "docs"],
        template=(
            "You are a helpful assistant that can answer questions and concerns "
            "about Google Cloud Certifications. You can help users with questions "
            "about the certification process, exam details, and project ideas. "
            "You can also provide information about the different certification "
            "paths and the benefits of getting certified. "
            "Answer the user's {question} based on the information provided here: {docs}"
        ),
    )

    # Create and invoke the chain
    chain = prompt | llm
    response = chain.invoke({"question": query, "docs": docs_text})
    return response


if __name__ == "__main__":
    print(ai_helper("How can I pass Associate Cloud Engineer exam?"))
