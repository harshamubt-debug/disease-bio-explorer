import streamlit as st
from Bio import Entrez
import pandas as pd
import plotly.express as px

Entrez.email = "your_email@gmail.com"

st.title("Disease Bio Explorer")

disease = st.text_input("Enter Disease Name")

if disease:

    search = Entrez.esearch(db="nucleotide", term=disease, retmax=1)
    record = Entrez.read(search)

    if len(record["IdList"]) > 0:

        genome_id = record["IdList"][0]

        fetch = Entrez.efetch(db="nucleotide", id=genome_id, rettype="gb", retmode="text")
        genome = fetch.read()

        st.subheader("Genome Information")
        st.text(genome[:800])

    st.subheader("More Resources")

    st.write("NCBI:", f"https://www.ncbi.nlm.nih.gov/search/all/?term={disease}")
    st.write("UniProt:", f"https://www.uniprot.org/uniprotkb?query={disease}")
    st.write("WHO Data:", "https://www.who.int/data")

# ----------- GLOBAL DATA VISUALIZATION -----------

st.subheader("Global Disease Data")

url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
data = pd.read_csv(url)

# ----------- CASES OVER TIME GRAPH -----------

st.subheader("Cases Over Time (India Example)")

india_data = data[data["location"] == "India"]

fig = px.line(
    india_data,
    x="date",
    y="total_cases",
    title="Total Disease Cases Over Time"
)

st.plotly_chart(fig)

# ----------- WORLD MAP -----------

st.subheader("Global Disease Distribution")

latest = data.sort_values("date").groupby("location").tail(1)

fig_map = px.choropleth(
    latest,
    locations="iso_code",
    color="total_cases",
    hover_name="location",
    title="Global Disease Cases"
)

st.plotly_chart(fig_map)
