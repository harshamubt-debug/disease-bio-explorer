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
        url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
        data = pd.read_csv(url)

    elif "dengue" in disease.lower():
        url = "https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world_population.csv"
        data = pd.read_csv(url)

    elif "malaria" in disease.lower():
        url = "https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world_population.csv"
        data = pd.read_csv(url)

except:
    st.warning("Could not load epidemiology dataset.")

# ----------- VISUALIZATION -----------

if data is not None:

    st.subheader("Global Distribution")

    country_col = data.columns[0]
    value_col = data.columns[-1]

    country_data = data.groupby(country_col)[value_col].sum().reset_index()

    fig_map = px.choropleth(
        country_data,
        locations=country_col,
        locationmode="country names",
        color=value_col
    )

    st.plotly_chart(fig_map)
