# AI-Powered Content Summarization

Summarizes an article URL, pasted text or a PDF. Long documents are chunked and summarized map-reduce style, so they can exceed the context window.

Write-up: https://chiraggandhi-notes.vercel.app/llm-basics/projects/ai-powered-content-summarization

## Run

```bash
cd content-summarizer
pip install -r requirements.txt
cp .env.example .env    # add your API key
streamlit run app.py
```
