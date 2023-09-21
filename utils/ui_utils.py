import streamlit as st
import transcript_audio.fetch_youtube_data as youtube
import pandas as pd
import plotly.express as px
from constants import BASE_URL


def get_query_data(query: str, results_from: str, background_sound: bool):
    if st.session_state.get(results_from).get(query) is None:
        status_container = st.empty()
        status_container.status("searching videos...")
        videos_id = youtube.get_valid_videos_id(
            query.replace("_", " "), status_container,background_sound
        )
        st.session_state.get(results_from)[query] = videos_id
        status_container.empty()


def videos_list(query: str, results_from: str):
    if st.session_state.get(results_from).get(query) is not None:
        videos = st.session_state.get(results_from)[query]
        selected_video = st.selectbox(f"search results : {len(videos)}", videos)
        if selected_video is not None:
            st.video(f"{BASE_URL}{selected_video}")


def visualize_categories(results_from: str):
    if st.session_state.get(results_from):
        all_videos = st.session_state.get(results_from)
        category_list = [category.replace("_", " ") for category in all_videos.keys()]
        df = pd.DataFrame(category_list, columns=["query"])
        no_of_category_videos = [len(videos) for videos in all_videos.values()]
        df["no_of_results"] = no_of_category_videos
        fig = px.pie(df, values="no_of_results", names="query")
        st.plotly_chart(fig)
