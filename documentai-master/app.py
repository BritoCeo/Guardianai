import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid
import pandas as pd
import json
import numpy as np

# Title of the app
st.title("Welcome to Guardian AI")

# Upload PDF file
uploaded_file = st.file_uploader('Choose your Invoice .pdf file', type=["pdf", "jpg", "jpeg", "png"])

# If the user uploads a PDF
if uploaded_file is not None:

    # Initialize empty arrays for names and values
    name_arr = []
    value_arr = []

    # Load JSON file that contains the extracted names and values
    with open("test/header.json", "r") as json_file:
        json_dict = json.load(json_file)

    # Convert JSON keys and values to numpy arrays
    name_arr = np.array(list(json_dict.keys()))
    value_arr = np.array(list(json_dict.values()))

    # Create the text inputs in the sidebar dynamically based on the size of the arrays
    with st.sidebar:
        for i in range(min(len(name_arr), len(value_arr), 10)):  # Limit to 10 fields max
            st.text_input(name_arr[i], value=value_arr[i])

    # Load the CSV file containing the invoice data
    df = pd.read_csv("test/page2_1.csv")

    # Configure the AG Grid table
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(value=True, enableRowGroup=True, aggFunc=None, editable=True)
    gb.configure_selection(selection_mode="multiple", use_checkbox=True)
    grid_options = gb.build()
    grid_options["columnDefs"][0]["headerCheckboxSelection"] = True

    # Create a form for submitting table changes
    with st.form("table_form", clear_on_submit=False):
        grid_response = AgGrid(df, gridOptions=grid_options, height=300,
                               data_return_mode="AS_INPUT", update_mode='MODEL_CHANGED')

        # Capture selected rows from the grid
        selected = grid_response['selected_rows']

        # On submit, update the DataFrame based on selected rows
        if st.form_submit_button("Submit"):
            df = pd.DataFrame(selected)
        else:
            df = grid_response['data']


    # Function to convert dataframe to CSV
    def convert_df(df):
        """Convert DataFrame to CSV."""
        return df.to_csv().encode('utf-8')

    # Generate CSV for download
    csv = convert_df(df)

    # Download button for the CSV
    st.download_button(
        "Press to Download",
        csv,
        "file.csv",
        "text/csv",
        key='download-csv'
    )