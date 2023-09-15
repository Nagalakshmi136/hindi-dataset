import streamlit as st
import plotly.express as px
import pandas as pd
import language_videos.fetch_youtube_data as youtube
import constants as ct

with st.form("query"):

    def get_query() -> str:
        query = st.text_input("Enter your search", placeholder="search...")
        is_submit = st.form_submit_button(
            "submit",
        )
        if is_submit:
            if st.session_state.get("videos_id") is not None:
                del st.session_state.videos_id
            return query

    query = get_query()
    if query is not None:
        videos_id = youtube.get_valid_videos_id(query)
        # videos_id = video_transcript.keys()
        if videos_id not in st.session_state:
            st.session_state.videos_id = videos_id
        if st.session_state.get("categories") is None:
            st.session_state.categories = []
        st.session_state.categories.append((query, len(videos_id)))


if st.session_state.get("videos_id") is not None:
    videos = st.session_state.videos_id
    selected_video = st.selectbox(f"search results : {len(videos)}", videos)
    if selected_video is not None:
        st.video(f"{ct.BASE_URL}{selected_video}")
if st.session_state.get("categories") is not None:
    df = pd.DataFrame(st.session_state.categories, columns=["query", "no_of_results"])
    result_df = df.drop_duplicates(subset=["query"], keep="last")
    fig = px.pie(result_df, values="no_of_results", names="query")
    st.plotly_chart(fig)
