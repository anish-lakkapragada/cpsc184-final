import streamlit as st

from analysis import trademark
from data_sources import TRADEMARK_SOURCES

st.title("Trademark Infringement Monitor")

brand = st.text_input("Brand name", placeholder="e.g. nike, rolex")
sources = st.multiselect(
    "Sources",
    options=list(TRADEMARK_SOURCES.keys()),
    default=list(TRADEMARK_SOURCES.keys()),
)
limit = st.slider("Listings per source", 20, 200, 100, step=10)

if st.button("Run", type="primary", disabled=not brand):
    all_items = []
    for name in sources:
        try:
            with st.spinner(f"Fetching from {name}..."):
                items = TRADEMARK_SOURCES[name].fetch(brand, limit=limit)
            all_items.extend(items)
            st.write(f"{name}: {len(items)} listings fetched")
        except Exception as e:
            st.error(f"{name} failed: {e}")

    if all_items:
        with st.spinner("Analyzing..."):
            report = trademark.analyze(brand, all_items)

        st.subheader(f"Results for '{brand}'")
        st.write(f"Scanned {report.total_scanned} listings, flagged {len(report.flagged)}")

        if not report.flagged:
            st.success("No suspicious listings found!")
        else:
            for f in report.flagged:
                with st.container(border=True):
                    st.markdown(f"**[{f.listing.title}]({f.listing.url})**")
                    st.caption(f"Seller: {f.listing.seller or '—'}  ·  Price: ${f.listing.price}")
