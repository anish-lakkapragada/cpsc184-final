import streamlit as st

st.set_page_config(page_title="Trademark & Genericide Monitor")
st.title("Trademark & Genericide Monitor")

st.markdown("""
A rule-based pipeline for two intellectual-property tasks:

- **Trademark infringement** — scans eBay listings for potential unauthorized
  uses of a brand name, using fuzzy title matching and seller heuristics.
- **Genericide detection** — measures how often a brand is used as a generic term
  vs. as a proper noun across Reddit and Hacker News, using spaCy POS rules.

Pick a page from the sidebar to get started.
""")
