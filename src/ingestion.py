from pathlib import Path
import json, yaml, hashlib
from langchain_community.document_loaders import WebBaseLoader, SitemapLoader, CSVLoader, PyPDFLoader, TextLoader, UnstructuredMarkdownLoader
from langchain_core.documents import Document
from tqdm import tqdm
from src.utils_text import html_to_markdown, normalize_text


RAW = Path("data/raw"); PRO = Path("data/processed")
RAW.mkdir(parents=True, exist_ok=True); PRO.mkdir(parents=True, exist_ok=True)


USER_AGENT = "rag-course-bot/1.0"


def _save(path: Path, text: str):
    path.write_text(text, encoding="utf-8")


def _hash(s: str) -> str:
    return hashlib.md5(s.encode("utf-8")).hexdigest()[:10]


# def ingest_from_yaml(cfg_path: str = "scripts/ingest_urls.yaml") -> list[Document]:
#     cfg = yaml.safe_load(Path(cfg_path).read_text(encoding="utf-8"))
#     docs: list[Document] = []


#     # URLs
#     for url in cfg.get("urls", []):
#         loader = WebBaseLoader([url], header_template={"User-Agent": USER_AGENT})
#         for doc in loader.load():
#             html = doc.page_content
#             md = html_to_markdown(html)
#             md = normalize_text(md)
#             hid = _hash(url)
#             _save(RAW / f"{hid}.html", html)
#             _save(PRO / f"{hid}.md", md)
#             docs.append(Document(page_content=md, metadata={"source": url}))


#     # Sitemaps (tự lọc pdf/md)
#     for sm in cfg.get("sitemaps", []):
#         sl = SitemapLoader(web_path=sm, filter_urls=[r".*"], header_template={"User-Agent": USER_AGENT})
#         for d in sl.load():
#             url = d.metadata.get("source", "")
#             md = normalize_text(d.page_content)
#             hid = _hash(url)
#             _save(PRO / f"{hid}.md", md)
#             docs.append(Document(page_content=md, metadata={"source": url}))


#     return docs


def ingest_local_files(patterns=("*.pdf","*.md","*.txt","*.csv")) -> list[Document]:
    docs: list[Document] = []
    for pat in patterns:
        for p in RAW.rglob(pat):
            if p.suffix.lower()==".pdf":
                for d in PyPDFLoader(str(p)).load():
                    docs.append(Document(page_content=normalize_text(d.page_content), metadata={"source": str(p)}))
            elif p.suffix.lower()==".md":
                for d in UnstructuredMarkdownLoader(str(p)).load():
                    docs.append(Document(page_content=normalize_text(d.page_content), metadata={"source": str(p)}))
            elif p.suffix.lower()==".txt":
                for d in TextLoader(str(p), encoding="utf-8").load():
                    docs.append(Document(page_content=normalize_text(d.page_content), metadata={"source": str(p)}))
            elif p.suffix.lower()==".csv":
                docs.extend(CSVLoader(str(p)).load())
    return docs