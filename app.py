import streamlit as st
import plotly.express as px
import pandas as pd
import language_videos.fetch_youtube_data as youtube

with st.form("query"):

    def get_query() -> str:
        query = st.text_input("Enter your search", placeholder="search...")
        is_submit = st.form_submit_button(
            "submit",
        )
        if is_submit:
            if st.session_state.get("transcript_video_ids") is not None:
                del st.session_state.transcript_video_ids
            return query

    query = get_query()
    if query is not None:
        video_transcript = youtube.get_video_transcripts(query)
        transcript_video_ids = video_transcript.keys()
        if transcript_video_ids not in st.session_state:
            st.session_state.transcript_video_ids = transcript_video_ids
        if st.session_state.get("categories") is None:
            st.session_state.categories = []
        st.session_state.categories.append([query, len(transcript_video_ids)])


if st.session_state.get("transcript_video_ids") is not None:
    videos = st.session_state.transcript_video_ids
    selected_video = st.selectbox(f"search results : {len(videos)}", videos)
    if selected_video is not None:
        st.video(f"https://www.youtube.com/watch?v={selected_video}")
if st.session_state.get("categories") is not None:
    df = pd.DataFrame(st.session_state.categories, columns=["query", "no_of_results"])
    fig = px.pie(df, values="no_of_results", names="query")
    st.plotly_chart(fig)
