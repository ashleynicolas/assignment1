"""Script creates a Streamlit app to interact with headline scoring API"""
import requests
import streamlit as st

st.title("Headline Sentiment Analyzer")

# Establish different session states for sending headlines to server vs receiving sentiment scoring
if "headlines" not in st.session_state:
    st.session_state["headlines"]=[""]
if "scores" not in st.session_state:
     st.session_state["scores"] = []

# Function dds a new text input box to add a headline
def add_headline():
    st.session_state["headlines"].append("")

# Function deletes the last headline added
def delete_headline():
    if len(st.session_state["headlines"]) > 1:
        st.session_state["headlines"].pop()

# Displays a new text input box
for i in range(len(st.session_state["headlines"])):
    st.session_state.headlines[i] = st.text_input("Please enter your headline here:",
                                               value = st.session_state["headlines"][i],
                                               key = f"Headline_{i}")

# Creates 3 buttons that sit next to each other on a page
col1, col2, col3 = st.columns(3)
with col1:
    st.button("Add a headline", on_click = add_headline)

with col2:
    st.button("Delete a headline",on_click = delete_headline)

# Sends the headlines to the server to be scored when a user clicks the "Score Headlines" button
with col3:
    if st.button("Score Headlines", type="primary"):
        headline_list = [i for i in st.session_state.headlines if i.strip()]
        if not headline_list:
                st.warning("Please add a headline before scoring.")
        else:
            try:
                response = requests.post(url = "http://127.0.0.1:8082/score_headlines", json=headline_list)
                response.raise_for_status()
                data = response.json()
                st.session_state.scores = data.get("labels", [])
            except requests.RequestException as e:
                st.error(f"Error connecting to server: {e}")
                st.session_state.scores = []

# Displays the sentiment scores for each headline
if st.session_state["scores"]:
     st.markdown("# Scores:")
     for headline,score in zip(headline_list, st.session_state.scores):
          st.markdown(f"**{headline}:** *{score}*")
