from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
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
    return HuggingFaceEmbeddings(model_name=SETTINGS.embedding_model)


def build_index(docs: list[Document]):
    chunks = splitter.split_documents(docs)
    embeddings = _get_embedder()
    vs = Chroma.from_documents(chunks, embedding=embeddings, persist_directory=CHROMA_DIR)
    vs.persist()
    return vs


def load_index():
    embeddings = _get_embedder()
    return Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)