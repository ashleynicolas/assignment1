"""Script creates a Streamlit app to interact with headline scoring API"""
import requests
import Streamlit as st

st.title("Headline Sentiment Analyzer")

if "headlines" not in st.session_state:
    st.session_state.headlines=[""]

def add_headline():
    st.session_state.headlines.append("")

def delete_headline(idx):
    if len(st.session_state.headlines) > 1:
        st.session_state.headlines.pop(idx)

col1, col2 = st.columns(2)

with col1:
    st.button("Add a headline", on_click = add_headline)

with col2:
    st.button("Delete a headline",on_click=delete_headline)

if st.button("Score Headlines"):
        response = requests.post(url = "http://127.0.0.1:8082/score_headlines", json=st.session_state.headlines)
        scores = response.json().get()
        st.markdown(scores)



