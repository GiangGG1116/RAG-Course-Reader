from typing import List
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from src.embed_index import load_index
from src.reranker import Reranker
from src.prompts import ANSWER_PROMPT
from src.config import SETTINGS


# Build retriever
_vectordb = load_index()
retriever = _vectordb.as_retriever(search_type="mmr", search_kwargs={"k": 20, "fetch_k": 40, "lambda_mult": 0.5})
reranker = Reranker()


# LLM provider
if SETTINGS.provider == "openai" and SETTINGS.openai_api_key:
    llm = ChatOpenAI(model=SETTINGS.openai_model, temperature=0.2)
else:
    llm = HuggingFaceEndpoint(repo_id=SETTINGS.hf_llm, max_new_tokens=512, temperature=0.2, repetition_penalty=1.05)


# Format context with indices for citations
def format_context(docs: List[Document]) -> str:
    lines = []
    for i, d in enumerate(docs, start=1):
        src = d.metadata.get("source", "")
        snippet = d.page_content[:800]
        lines.append(f"[{i}] {snippet}\n(Source: {src})")
    return "\n\n".join(lines)


# Full chain: Retrieve → Rerank → Generate → (Cite inside answer)


def get_answer(question: str, top_k: int = 6):
    # 1) Retrieve
    raw_docs = retriever.get_relevant_documents(question)
    # 2) Rerank
    reranked = reranker.rerank(question, raw_docs)[:top_k]
    # 3) Generate
    chain = (
        {"context": lambda x: format_context(reranked), "question": RunnablePassthrough()}
        | ANSWER_PROMPT
        | llm
        | StrOutputParser()
    )
    answer = chain.invoke(question)
    return answer, reranked