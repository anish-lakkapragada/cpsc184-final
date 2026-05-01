import re

import streamlit as st

from analysis import genericide
from data_sources import GENERICIDE_SOURCES


def snippet(text, brand, window=140):
    text = re.sub(r"\s+", " ", text).strip()
    idx = text.lower().find(brand.lower())
    if idx < 0:
        return text[:300]
    start = max(0, idx - window)
    end = min(len(text), idx + len(brand) + window)
    s = text[start:end]
    if start > 0:
        s = "…" + s
    if end < len(text):
        s = s + "…"
    return re.sub("(?i)" + re.escape(brand), f"**{brand}**", s)

st.title("Genericide Detection")

brand = st.text_input("Brand name", placeholder="e.g. google, uber, xerox")
sources = st.multiselect(
    "Sources",
    options=list(GENERICIDE_SOURCES.keys()),
    default=list(GENERICIDE_SOURCES.keys()),
)
limit = st.slider("Mentions per source", 20, 200, 100, step=10)

if st.button("Run", type="primary", disabled=not brand):
    all_mentions = []
    for name in sources:
        try:
            with st.spinner(f"Fetching from {name}..."):
                items = GENERICIDE_SOURCES[name].fetch(brand, limit=limit)
            all_mentions.extend(items)
            st.write(f"{name}: {len(items)} mentions fetched")
        except Exception as e:
            st.error(f"{name} failed: {e}")

    if all_mentions:
        with st.spinner("Analyzing..."):
            report = genericide.analyze(brand, all_mentions)

        st.subheader(f"Results for '{brand}'")
        total = report.generic_count + report.branded_count

        if total == 0:
            st.warning("Brand not found in any mentions.")
        else:
            st.metric("Genericide Risk Score", f"{round(report.ratio * 100, 1)}%")

            col1, col2 = st.columns(2)
            col1.metric("Generic uses", report.generic_count)
            col2.metric("Branded uses", report.branded_count)

            if report.examples_generic:
                st.subheader("Generic examples")
                for m in report.examples_generic:
                    st.caption(snippet(m.text, brand))

            if report.examples_branded:
                st.subheader("Branded examples")
                for m in report.examples_branded:
                    st.caption(snippet(m.text, brand))
