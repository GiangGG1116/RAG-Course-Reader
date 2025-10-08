from langchain_core.documents import Document
from collections import defaultdict
import hashlib, re


HEADING_RE = re.compile(r"^#+ ", re.M)


def deduplicate(docs: list[Document]) -> list[Document]:
    seen = set(); out = []
    for d in docs:
        h = hashlib.md5(d.page_content.encode("utf-8")).hexdigest()
        if h not in seen:
            seen.add(h); out.append(d)
    return out


def enrich_metadata(docs: list[Document]) -> list[Document]:
    for d in docs:
        txt = d.page_content
        d.metadata.setdefault("n_chars", len(txt))
        d.metadata.setdefault("n_headings", len(HEADING_RE.findall(txt)))
    return docs