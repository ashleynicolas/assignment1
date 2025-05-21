"""Script creates a Streamlit app to interact with headline scoring API"""
import requests
import streamlit as st

st.title("Headline Sentiment Analyzer")

if "headlines" not in st.session_state:
    st.session_state.headlines=[""]

def add_headline():
    st.session_state.headlines.append("")

def delete_headline():
    if len(st.session_state.headlines) > 1:
        st.session_state.headlines.pop()

st.session_state.headlines[idx] = st.text_input("Please enter your headline here", 
                                                value = st.session_state.headlines[idx],
                                                key = f"Headlines_{idx+1}")

col1, col2 = st.columns(2)

with col1:
    headline_input = st.text_input("Please enter headline below:")
    st.button("Add a headline", on_click = add_headline)

with col2:
    st.button("Delete a headline",on_click=delete_headline)

if st.button("Score Headlines"):
        headlines = [headline for headline in st.session_state.headlines]
        response = requests.post(url = "http://127.0.0.1:8082/score_headlines", json=headlines)
        scores = response.json().get("Sentiment Scores",[])
        for headline, score in zip(headlines, scores):
             st.markdown(f"##{headline}: *{score}*")
