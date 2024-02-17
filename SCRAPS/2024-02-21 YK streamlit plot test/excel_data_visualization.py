import streamlit as st
import pandas as pd
import plotly.express as px

# Function to read Excel file
def read_excel(file):
    try:
        df = pd.read_excel('streamlit_test.xlsx')
        return df
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Function to visualize data
def visualize_data(df):
    try:
        fig = px.line(df, x='Date', y=df.columns[1:], title='Time Series Data')
        st.plotly_chart(fig)
    except Exception as e:
        st.error(f"An error occurred: {e}")

def main():
    st.title('Excel Data Visualization App')
    
    # Upload Excel file
    uploaded_file = st.file_uploader("Upload Excel file", type=['xlsx', 'xls'])
    
    if uploaded_file is not None:
        # Read Excel file
        df = read_excel(uploaded_file)
        if df is not None:
            # Display first few rows of the data
            st.write("Data Preview:")
            st.write(df.head())
            
            # Visualize data
            visualize_data(df)

if __name__ == "__main__":
    main()
