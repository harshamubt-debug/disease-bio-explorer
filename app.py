import streamlit as st
from Bio import Entrez
import pandas as pd
import plotly.express as px

Entrez.email = "your_email@gmail.com"

st.title("Disease Bio Explorer")

disease = st.text_input("Enter Disease Name")

# ----------- GENOME DATA FROM NCBI -----------

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

# ----------- GLOBAL DISEASE DATA -----------

st.subheader("Global Disease Analytics")

data = None

try:

    if "covid" in disease.lower():
        url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
        data = pd.read_csv(url)

    elif "dengue" in disease.lower():
        url = "https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv"
        data = pd.read_csv(url)

    elif "malaria" in disease.lower():
        url = "https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv"
        data = pd.read_csv(url)

except Exception as e:
    st.error("Could not load epidemiology dataset.")
# ----------- VISUALIZATION -----------

if data is not None:

    st.subheader("Global Distribution Map")

    if "covid" in disease.lower():

        latest = data.sort_values("date").groupby("location").tail(1)

        fig_map = px.choropleth(
            latest,
            locations="iso_code",
            color="total_cases",
            hover_name="location",
            title="Global COVID Cases"
        )

        st.plotly_chart(fig_map)

    else:

        fig_map = px.choropleth(
            data,
            locations="CODE",
            color="GDP (BILLIONS)",
            hover_name="COUNTRY",
            title="Global Distribution Example"
        )

        st.plotly_chart(fig_map)
