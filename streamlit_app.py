"""Script creates a Streamlit app to interact with headline scoring API"""
import requests
import streamlit as st

st.title("Headline Sentiment Analyzer")

def headlines_list():
    if "headlines" not in st.session_state:
        st.session_state.headlines=[""]
        st.session_state.next_key = 1

def add_headline():
    st.session_state.headlines.append("")
    st.session_state.next_key += 1
    st.experimental_rerun()

def delete_headline(idx):
    if len(st.session_state.headlines) > 1:
        st.session_state.headlines.pop(idx)
        st.experimental_rerun()
        
headlines_list()

col1, col2 = st.columns(2)

with col1:
    headline_input = st.text_input("Please enter headline below:")
    st.button("Add a headline", on_click = add_headline)

with col2:
    st.button("Delete a headline",on_click=delete_headline)

def score_headlines():
    response = requests.post(url = "http://127.0.0.1:8082/score_headlines", json=st.session_state.headlines)
    scores = response.json().get()
    st.markdown(scores)

if st.button("Score Headlines", on_click=score_headlines):
    pass

