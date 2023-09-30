"""
Search page i.e. you can search desired data by giving query
"""
import streamlit as st

from utils.ui_utils import get_query_data, videos_list, visualize_categories

# Storing the results temporarily in between reloads using session state
if st.session_state.get("results_from_search") is None:
    st.session_state.results_from_search = {}
if st.session_state.get("query") is None:
    st.session_state.query = ""
if st.session_state.get("background_sound") is None:
    st.session_state.background_sound = True

# Load and process data from query only when submit button clicks which achieved by form
with st.form("search_form"):
    query = st.text_input("Enter your search", placeholder="search...").replace(
        " ", "_"
    )
    radio_option = st.radio("About background sound:", ["Enable", "Disable"])
    if radio_option == "Disable":
        st.session_state.background_sound = False
    is_submit = st.form_submit_button(
        "submit",
    )
    if is_submit and query is not None:
        st.session_state.query = query
        get_query_data(query, "results_from_search")
        
# List of video satisfies the given query
videos_list(st.session_state.query, "results_from_search")
# Visualizing the no.of videos in each query or category
visualize_categories("results_from_search")
