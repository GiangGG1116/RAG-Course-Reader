from typing import List, Tuple
from dataclasses import dataclass
from sentence_transformers import CrossEncoder
from src.config import SETTINGS


@dataclass
class ScoredDoc:
    doc: any
    score: float


class Reranker:
    def __init__(self):
        self.model = CrossEncoder(SETTINGS.reranker_model)


    def rerank(self, query: str, docs: list) -> list:
        pairs = [(query, d.page_content) for d in docs]
        scores = self.model.predict(pairs)
        rescored = sorted([ScoredDoc(d, float(s)) for d,s in zip(docs, scores)], key=lambda x: -x.score)
        return [x.doc for x in rescored]