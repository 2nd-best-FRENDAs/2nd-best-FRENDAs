import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objs as go
import tellurium as te
import numpy as np

### FUNCTIONS!!!!!!!!!

# Upload CSV file
def upload_file():
    st.header("upload files")
    file = st.file_uploader('Upload CSV', type=['csv'])
    df = pd.read_csv(file)
    if df is not None:
        # Display first few rows of the data
        st.write("Data Preview:")
        st.write(df.head())
        st.session_state.df = df
        return df
    else:
        st.error(f"An error occurred")
        return None
        
# Convert df file to SBML readable format
def convert_to_sbml(df, filetype):
    model_content = df.to_csv(index=False)
    if filetype=='antimony':
        try:
            model_sbml = te.antimonyToSBML(model_content)
            model_load = te.loadSBMLModel(model_sbml)
            st.success(f"Successfully converted file file from {filetype} to SBML and loaded.")
        except Exception as e:
            st.error("Could not load file.", e)
    else: 
        try:
            model_load = te.loadSBMLModel(model_content)
            st.success(f"Successfully loaded SBML file.")
        except Exception as e:
            st.error("Could not load SBML file.", e)
    return model_load
    
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
        st.write("Please upload a CSV file first.")

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
        x_column = st.selectbox('Select X Column:', options=columns)
        y_columns = [col for col, selected in zip(columns, selected_columns) if selected and col != x_column]
        if y_columns:
            fig = generate_plot(df, x_column, y_columns)
            st.plotly_chart(fig)
        else:
            st.write('No Y columns selected.')
        # Print selected columns
        st.write('Selected Y Columns:', [col for col, selected in zip(columns, selected_columns) if selected and col != x_column])
    else:
        st.write("Please upload a CSV file first.")

### MAIN STREAMLIT APP CODE!!!!!!!!!!!!!!
def main():
    st.title('Compound Time Visualization')

    # Create tabs
    tabs = ["Upload file", "Convert to SBML", "Plot all", "Plot selected"]
    selected_tab = st.sidebar.radio("Select Page", tabs)

    # Page 1 content
    if selected_tab == "Upload file": 
        upload_file()
    
    elif selected_tab == "Convert to SBML":
        st.header("Convert CSV to SBML")
        st.subheader("Upload a CSV file first to convert it to SBML format.")
        if st.session_state.df is not None:
            if st.button("Convert"):
                convert_to_sbml(st.session_state.df)
                st.success("Conversion successful!")
    
    # Page 2 content
    elif selected_tab == "Plot all":
        visualize_data()

    #page 3
    elif selected_tab == "Plot selected":
        custom_plot()
        

if __name__ == "__main__":
    main()
