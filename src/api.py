from fastapi import FastAPI, Body
from pydantic import BaseModel
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
from src.ingestion import ingest_local_files
from src.preprocess import deduplicate, enrich_metadata
from src.embed_index import build_index, load_index
from src.generate import get_answer
from src.monitor import REQUESTS, RETRIEVAL_LAT, GEN_LAT, Timer


app = FastAPI(title="RAG Course API", version="1.0")


class AskReq(BaseModel):
    question: str
    top_k: int = 6


@app.post("/ingest")
def ingest():
    # docs = ingest_from_yaml()
    docs += ingest_local_files()
    docs = enrich_metadata(deduplicate(docs))
    build_index(docs)
    return {"ok": True, "n_docs": len(docs)}


@app.post("/ask")
def ask(req: AskReq):
    REQUESTS.inc()
    with Timer() as t1:
        answer, ctx = get_answer(req.question, req.top_k)
    return {
        "answer": answer,
        "sources": [{"source": d.metadata.get("source"), "chars": d.metadata.get("n_chars")} for d in ctx],
        "latency_s": t1.dt,
    }


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)