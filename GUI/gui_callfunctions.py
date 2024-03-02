import streamlit as st

import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objs as go
import tellurium as te
import numpy as np
import base64

from functions_to_import import load_model, simulate_model

### FUNCTIONS!!!!!!!!!
def upload_model():
    st.header("upload your model here")
    # Selectbox to choose between "antimony" and "sbml"
    selected_option = st.selectbox("Select your model type", ["antimony", "sbml"])
    uploaded_file = st.file_uploader('Upload file')

    if uploaded_file is not None:
        # Display the file name if file is uploaded
        file_name = uploaded_file.name
        st.write("Your uploaded file name:", file_name)

        # Display the file contents
        file_content = uploaded_file.read()
        model_load = load_model(file_content, selected_option)
        
        st.write("Success!!!!!!! File contents:")
        st.write(model_load)

        st.session_state.uploaded_file = uploaded_file
        st.session_state.model_load = model_load
    else:
        st.write("Please upload a file")

def solve_model():
    st.header("fill out info below to solve your model in tellurium")

    #inputs
    t0 = st.number_input("Enter your t0", value=0)
    t1 = st.number_input("Enter your t1", value=0)
    steps = st.number_input("Enter the number of steps you want", value=0)

    # Button to trigger processing
    if st.button("Solve Model"):
        if "model_load" in st.session_state:
            model_load = st.session_state.model_load
            try:
                df = simulate_model(model_load, t0, t1, steps)
                # returns result, df, species_names
                st.write(df.head())
                st.session_state.df = df
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.write("load model first")
    

    # Button to download the DataFrame as a CSV file
    if st.button("Download CSV"):
        # Create a link to download the CSV file
        if "df" in st.session_state:
            df = st.session_state.df
            try:
                csv = df.to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()  # Convert DataFrame to bytes
                href = f'<a href="solved_model:file/csv;base64,{b64}" download="solved_model.csv">Download CSV File</a>'
                st.markdown(href, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.write("load model first")


##### PLOTTING!!!!!!!!!!!!!!!!!!!
# Function to generate plot
def visualize_data():
    st.header("All data")
    if "df" in st.session_state:
        df = st.session_state.df
        try:
            fig = px.line(df, x=df.columns[0], y=df.columns[1:], title='Time Series Data')
            st.plotly_chart(fig)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.write("load model first")
# Function to generate plot with selected columns
def generate_plot(df, x_column, y_columns):
    fig = go.Figure()
    for y_column in y_columns:
        fig.add_trace(go.Scatter(x=df[x_column], y=df[y_column], mode='lines', name=y_column))
    fig.update_layout(title='Customizable Plot', xaxis_title=x_column, yaxis_title='Value')
    return fig
def custom_plot():
    st.header("Customizable Plot")
    if "df" in st.session_state:
        df = st.session_state.df
        # Display available columns and checkboxes
        st.write('Select Columns:')
        columns = df.columns.tolist()
        selected_columns = [st.checkbox(col, value=False) for col in columns]
        # Generate plot
        x_column = st.selectbox('Select X axis data:', options=columns)
        y_columns = [col for col, selected in zip(columns, selected_columns) if selected and col != x_column]
        if y_columns:
            fig = generate_plot(df, x_column, y_columns)
            st.plotly_chart(fig)
        else:
            st.write('No Y columns selected.')
        # Print selected columns
        #st.write('Selected Y Columns:', [col for col, selected in zip(columns, selected_columns) if selected and col != x_column])
    else:
        st.write("load model first")



### MAIN STREAMLIT APP CODE!!!!!!!!!!!!!!
def main():
    st.title('Compound Time Visualization')

    # Create tabs
    tabs = ["Upload model", "Solve model", "Plot all", "Plot selected"]
    selected_tab = st.sidebar.radio("Select Page", tabs)

    # Page 1 content
    if selected_tab == "Upload model": 
        upload_model()

    elif selected_tab == "Solve model":
        solve_model()

    elif selected_tab == "Plot all":
        visualize_data()

    elif selected_tab == "Plot selected":
        custom_plot()
        

if __name__ == "__main__":
    main()
