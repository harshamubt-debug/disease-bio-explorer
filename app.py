
import streamlit as st

st.title("🌍 Global Disease Bio Explorer")

disease = st.text_input("Enter Disease Name")

if disease:
    st.write("You searched for:", disease)
