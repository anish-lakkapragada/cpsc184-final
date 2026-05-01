import streamlit as st

st.set_page_config(page_title="CPSC 184 Final Project: Trademark & Genericide Monitor 3000")
st.title("CPSC 184 Final Project")

st.markdown("""
This is my final project for CPSC 184. Please click on one of the following tabs to get started: 

- **Trademark infringement**: scans eBay product listings for potential unauthorized
  uses of a brand name, using fuzzy search and some heuristics 

- **Genericide detection**: uses parts-of-speech (PoS) tagging to detect 
  if a brand name is being used generically. Pulls from Hacker News and Reddit.

Both give "reports" indicating the risk at which a brand name is at risk of trademark infringement 
or genericide. Thank you!  
""")
