import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objs as go

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
    else:
        st.error(f"An error occurred")
        return None

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
    tabs = ["upload file", "plot all", "plot selected"]
    selected_tab = st.sidebar.radio("Select Page", tabs)

    # Page 1 content
    if selected_tab == "upload file": 
        upload_file()
        
    # Page 2 content
    elif selected_tab == "plot all":
        visualize_data()

    #page 3
    elif selected_tab == "plot selected":
        custom_plot()


if __name__ == "__main__":
    main()
