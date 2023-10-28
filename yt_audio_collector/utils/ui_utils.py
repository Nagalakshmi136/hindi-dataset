"""
This module contains commonly used ui methods for the application.
"""
import pandas as pd
import plotly.express as px
import streamlit as st

from yt_audio_collector.transcript_audio.fetch_youtube_data import get_valid_video_ids
from constants import BASE_URL


def get_query_data(query: str, results_from: str) -> None:
    """
    Fetches the results of a query and stores the results in session state.

    Parameters:
    -----------
    query: `str`
        The query to search for.
    results_from: `str`
        The page from which the data is being requested.
    """

    if st.session_state.get(results_from).get(query) is None:
        status_container = st.empty()

        status_container.status("searching videos...")
        videos_id = get_valid_video_ids(query, status_container)
        st.session_state.get(results_from)[query] = videos_id
        status_container.empty()


def videos_list(query: str, results_from: str) -> None:
    """
    Displays a list of videos that satisfy the given query in session state.

    Parameters:
    -----------
    query: `str`
        The query to search for.
    results_from: `str`
        The page from which the data is being requested.
    """
    if st.session_state.get(results_from).get(query) is not None:
        st.write("## List of videos")
        videos = st.session_state.get(results_from)[query]
        selected_video = st.selectbox(f"search results : {len(videos)}", videos)
        if selected_video is not None:
            st.video(f"{BASE_URL}{selected_video}")


def visualize_categories(results_from: str):
    """
    Displays a pie chart of the number of videos in each query or category.

    Parameters:
    -----------
    results_from: `str`
        The page from which the data is being requested.
    """
    if st.session_state.get(results_from):
        st.write("## Category Distribution")
        all_videos = st.session_state.get(results_from)
        data_frame = pd.DataFrame(
            {
                "query": list(all_videos.keys()),
                "no.of_results": [len(v) for v in all_videos.values()],
            }
        )
        data_frame["query"].replace("_", " ", regex=True, inplace=True)
        fig = px.pie(data_frame, values="no.of_results", names="query")
        st.plotly_chart(fig)
