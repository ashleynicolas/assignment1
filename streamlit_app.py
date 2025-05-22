"""Script creates a Streamlit app to interact with headline scoring API"""
import requests
import streamlit as st

st.title("Headline Sentiment Analyzer")

# Check of \\\\
if "headlines" not in st.session_state:
    st.session_state["headlines"]=[""]
if "scores" not in st.session_state:
     st.session_state["scores"] = []

def add_headline():
    st.session_state["headlines"].append("")

def delete_headline():
    if len(st.session_state["headlines"]) > 1:
        st.session_state["headlines"].pop()

for idx in range(len(st.session_state["headlines"])):
    st.session_state.headlines = st.text_input("Please enter your headline here:",
                                               value = st.session_state["headlines"][idx],
                                               key = f"Headlines_{idx}")

col1, col2 = st.columns(2)
with col1:
    st.button("Add a headline", on_click = add_headline)

with col2:
    st.button("Delete a headline",on_click=delete_headline)

if st.button("Score Headlines"):
    response = requests.post(url = "http://127.0.0.1:8082/score_headlines", json=st.session_state.headlines)
    response.raise_for_status()
    data = response.json()
    st.session_state.scores = data.get("labels", [])

if st.session_state["scores"]:
     st.markdown("#Scores:")
     for headline,score in st.session_state.headlines, st.session_state.scores:
          st.markdown(f"###{headline}: **{score}")
