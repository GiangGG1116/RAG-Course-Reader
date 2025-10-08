import re, unicodedata
from bs4 import BeautifulSoup
from readability import Document
from markdownify import markdownify as md


def normalize_text(s: str) -> str:
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def html_to_markdown(html: str) -> str:
    # Ưu tiên lấy main content bằng readability
    try:
        article = Document(html).summary()
    except Exception:
        article = html
    soup = BeautifulSoup(article, "lxml")
    # bỏ script/style/nav/footer
    for t in soup(["script","style","nav","footer","header","noscript"]):
        t.decompose()
    return md(str(soup))