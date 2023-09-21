import streamlit as st
from utils.ui_utils import videos_list
from utils.ui_utils import get_query_data
from utils.ui_utils import visualize_categories
import transcript_audio.fetch_youtube_data as youtube
import constants as ct

if st.session_state.get("results_from_search") is None:
    st.session_state.results_from_search = {}
if st.session_state.get("query") is None:
    st.session_state.query = ""


def get_query() -> str:
    query = st.text_input("Enter your search", placeholder="search...")
    background_sound = st.radio("Disable background sound")
    is_submit = st.form_submit_button(
        "submit",
    )
    if is_submit:
        return query.replace(" ", "_"), background_sound


with st.form("search_form"):
    query, background_sound = get_query()
    if query is not None:
        st.session_state.query = query
        get_query_data(query, "results_from_search",background_sound)

videos_list(st.session_state.query, "results_from_search")
visualize_categories("results_from_search")
