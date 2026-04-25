import streamlit as st

from analysis import genericide
from data_sources import GENERICIDE_SOURCES



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
            with st.spinner("Fetching from " + name + "..."):
                items = GENERICIDE_SOURCES[name].fetch(brand, limit=limit)

            all_mentions.extend(items)
            st.write(name + ": " + str(len(items)) + " mentions fetched")

        except Exception as e:
            st.error(name + " failed: " + str(e))


    if all_mentions:

        with st.spinner("Analyzing..."):
            report = genericide.analyze(brand, all_mentions)


        st.subheader("Results for '" + brand + "'")


        total = report.generic_count + report.branded_count

        if total == 0:
            st.warning("Brand not found in any mentions.")

        else:

            st.metric("Genericide Risk Score", str(round(report.ratio * 100, 1)) + "%")

            col1, col2 = st.columns(2)
            col1.metric("Generic uses", report.generic_count)
            col2.metric("Branded uses", report.branded_count)


            if report.examples_generic:
                st.subheader("Generic examples")
                for m in report.examples_generic:
                    st.caption(m.text[:300])


            if report.examples_branded:
                st.subheader("Branded examples")
                for m in report.examples_branded:
                    st.caption(m.text[:300])
