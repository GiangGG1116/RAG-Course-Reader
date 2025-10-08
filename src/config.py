from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="/home/giangg1/project_CV/RAG/.env.example")

class Settings(BaseModel):
    provider: str = os.getenv("PROVIDER", "openai")
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    # hf_token: str | None = os.getenv("HF_TOKEN")


    # embedding_model: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    reranker_model: str = os.getenv("RERANKER_MODEL", "BAAI/bge-reranker-large")


    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    # hf_llm: str = os.getenv("HF_LLM", "mistralai/Mixtral-8x7B-Instruct-v0.1")


    chroma_dir: str = os.getenv("CHROMA_DIR", "./storage/chroma")


SETTINGS = Settings()