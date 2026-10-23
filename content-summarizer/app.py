import streamlit as st
from summarize import from_pdf, from_url, summarize

st.title("Summarizer")
style = st.selectbox("Style", ["5 concise bullet points", "a one-paragraph TL;DR",
                               "an executive summary with key takeaways"])
tab_url, tab_text, tab_pdf = st.tabs(["URL", "Text", "PDF"])

text = ""
with tab_url:
    url = st.text_input("Article URL")
    if url: text = from_url(url)
with tab_text:
    pasted = st.text_area("Paste text", height=250)
    if pasted: text = pasted
with tab_pdf:
    pdf = st.file_uploader("Upload PDF", type="pdf")
    if pdf: text = from_pdf(pdf)

if st.button("Summarize", disabled=not text):
    with st.spinner("Summarizing..."):
        st.markdown(summarize(text, style))
