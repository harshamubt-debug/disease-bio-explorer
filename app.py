import streamlit as st
from Bio import Entrez

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
