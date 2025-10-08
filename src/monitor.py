import time
from prometheus_client import Counter, Histogram


REQUESTS = Counter("rag_requests_total", "Total RAG /ask requests")
RETRIEVAL_LAT = Histogram("rag_retrieval_seconds", "Latency of retrieval")
GEN_LAT = Histogram("rag_generation_seconds", "Latency of generation")


class Timer:
    def __enter__(self):
        self.t0 = time.time(); return self
    def __exit__(self, *exc):
        self.dt = time.time() - self.t0