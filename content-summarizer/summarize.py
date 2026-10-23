import anthropic
import trafilatura
from dotenv import load_dotenv
from pypdf import PdfReader

load_dotenv()
client = anthropic.Anthropic()
MODEL = "claude-haiku-5-5"
CHUNK_TOKENS = 20_000          # well under the context window
CHARS_PER_TOKEN = 4            # rough estimate for chunking


# ---------- extraction ----------
def from_url(url: str) -> str:
    html = trafilatura.fetch_url(url)
    return trafilatura.extract(html) or ""

def from_pdf(file) -> str:
    return "\n".join(page.extract_text() or "" for page in PdfReader(file).pages)


# ---------- LLM ----------
def llm(prompt: str, max_tokens: int = 1024) -> str:
    resp = client.messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        temperature=0.2,       # faithful, not creative
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.content[0].text

def summarize_once(text: str, style: str) -> str:
    return llm(f"""Summarize the document below as {style}.
Only include information stated in the document. Do not add outside facts.

<document>
{text}
</document>""")


# ---------- chunking + map-reduce ----------
def chunk(text: str, size_tokens: int = CHUNK_TOKENS, overlap_tokens: int = 500):
    size, overlap = size_tokens * CHARS_PER_TOKEN, overlap_tokens * CHARS_PER_TOKEN
    start = 0
    while start < len(text):
        yield text[start:start + size]
        start += size - overlap

def summarize(text: str, style: str = "5 concise bullet points") -> str:
    tokens = client.messages.count_tokens(
        model=MODEL, messages=[{"role": "user", "content": text}]
    ).input_tokens

    if tokens <= CHUNK_TOKENS:
        return summarize_once(text, style)

    # map: summarize each chunk
    partials = [summarize_once(c, "a detailed paragraph") for c in chunk(text)]
    # reduce: summarize the summaries
    return summarize_once("\n\n".join(partials), style)
