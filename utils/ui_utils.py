import pandas as pd
import plotly.express as px
import streamlit as st

import transcript_audio.fetch_youtube_data as youtube
from constants import BASE_URL


def get_query_data(query: str, results_from: str) -> None:
    """
     Fetch the results of query and store the results in session state

    Parameters:
    ----------- 
    query: `str`
        represents the data you need
    results_from: `str`
        from which page data is requesting
    """

    if st.session_state.get(results_from).get(query) is None:
        status_container = st.empty()

        status_container.status("searching videos...")
        videos_id = youtube.get_valid_video_ids(query, status_container)
        st.session_state.get(results_from)[query] = videos_id
        status_container.empty()


def videos_list(query: str, results_from: str) -> None:
    """
    List of videos satisfies the given query in session state

    Parameters:
    ----------- 
    query: `str`
        represents the data you need

    results_from: `str`
        from which page data is requesting

    """
    if st.session_state.get(results_from).get(query) is not None:
        st.write('## List of videos')
        videos = st.session_state.get(results_from)[query]
        selected_video = st.selectbox(f"search results : {len(videos)}", videos)
        if selected_video is not None:
            st.video(f"{BASE_URL}{selected_video}")


def visualize_categories(results_from: str):
    """Visualizing the no.of videos in each query or category

    Args:
        results_from (str): from which page data is requesting
    """
    if st.session_state.get(results_from):
        st.write('## Category Distribution')
        all_videos = st.session_state.get(results_from)
        df = pd.DataFrame(
            {
                "query": list(all_videos.keys()),
                "no.of_results": [len(v) for v in all_videos.values()],
            }
        )
        df["query"].replace("_", " ", regex=True, inplace=True)
        fig = px.pie(df, values="no.of_results", names="query")
        st.plotly_chart(fig)
