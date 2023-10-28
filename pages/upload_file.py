"""
Upload file page i.e. you can give a text file 
with list of queries and get desired data.
"""
import streamlit as st

from yt_audio_collector.utils.ui_utils import (
    get_query_data,
    videos_list,
    visualize_categories,
)

# Storing the results temporarily in between reloads using session state
if st.session_state.get("results_from_upload") is None:
    st.session_state.results_from_upload = {}
if st.session_state.get("background_sound") is None:
    st.session_state.background_sound = True
# Load and process data from file only when submit button clicks which achieved by form
with st.form("upload_form"):
    uploaded_file = st.file_uploader("Upload your file here...")
    radio_option = st.radio("About background sound", ["Enable", "Disable"])
    if radio_option == "Disable":
        st.session_state.background_sound = False

    st.form_submit_button("upload")

    if uploaded_file is not None:
        # Fetching the uploaded file data i.e. list of queries
        file_data = uploaded_file.getvalue().decode("utf-8")
        queries_list = file_data.rstrip("\n").split(",")

        # Traversing each query and fetching corresponding data
        for query in queries_list:
            get_query_data(query.replace(" ", "_"), "results_from_upload")
# List of categories or queries names
if st.session_state.get("results_from_upload"):
    st.write("## List of Categories")
    categories_list = st.session_state.get("results_from_upload").keys()
    selected_category = st.selectbox("select category: ", categories_list)
    # List of videos corresponding to each query or category
    videos_list(selected_category, "results_from_upload")
# Visualizing the no.of videos in each query or category with pie chart
visualize_categories("results_from_upload")
