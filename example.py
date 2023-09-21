import streamlit as st

# Define the options for the outer selectbox
outer_options = ["Option 1", "Option 2", "Option 3"]

# Define the options for the inner selectbox
inner_options = {
    "Option 1": ["Suboption 1", "Suboption 2", "Suboption 3"],
    "Option 2": ["Suboption 4", "Suboption 5", "Suboption 6"],
    "Option 3": ["Suboption 7", "Suboption 8", "Suboption 9"],
}

# Create the outer selectbox
outer_selection = st.selectbox("Select an option:", outer_options)

# Create the inner selectbox based on the outer selection
inner_selection = st.selectbox("Select a suboption:", inner_options[outer_selection])
