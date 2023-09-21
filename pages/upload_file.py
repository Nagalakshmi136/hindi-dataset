from io import StringIO
import streamlit as st
from utils.ui_utils import get_query_data
from utils.ui_utils import visualize_categories
from utils.ui_utils import videos_list

if st.session_state.get("results_from_upload") is None:
    st.session_state.results_from_upload = {}

with st.form("upload_form"):
    uploaded_file = st.file_uploader("Upload your file here...")
    background_sound = st.radio("Disable background sound")
    st.form_submit_button("upload")

    if uploaded_file is not None:
        file_data = uploaded_file.getvalue().decode("utf-8")
        queries_list = file_data.split(",")

        for query in queries_list:
            get_query_data(query, "results_from_upload", background_sound)

if st.session_state.get("results_from_upload"):
    categories_list = st.session_state.get("results_from_upload").keys()
    selected_category = st.selectbox("select category: ", categories_list)
    videos_list(selected_category, "results_from_upload")

visualize_categories("results_from_upload")
