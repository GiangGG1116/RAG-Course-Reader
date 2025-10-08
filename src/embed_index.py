from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from src.config import SETTINGS


CHROMA_DIR = SETTINGS.chroma_dir


splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150,
    separators=["\n\n", "\n", " ", ""]
)


def _get_embedder():
    if SETTINGS.openai_api_key and SETTINGS.provider=="openai":
        return OpenAIEmbeddings(model="text-embedding-3-large")
    # return HuggingFaceEmbeddings(model_name=SETTINGS.embedding_model)


def build_index(docs: list[Document]):
    chunks = splitter.split_documents(docs)
    embeddings = _get_embedder()
    vs = Chroma.from_documents(chunks, embedding=embeddings, persist_directory=CHROMA_DIR)
    vs.persist()
    return vs


def load_index():
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large",OPENAI_API_KEY=SETTINGS.openai_api_key)
    return Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)

if __name__ == "__main__":
    # Test
    from src.ingestion import ingest_local_files
    docs = ingest_local_files()
    print(f"Ingested {len(docs)} documents")
    build_index(docs)
    print("Index built and saved.")
