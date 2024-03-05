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
def tab1_upload_model():
    st.header("upload your model here")
    # Selectbox to choose between "antimony" and "sbml"
    selected_option = st.selectbox("Select your model type", ["antimony", "sbml"])
    uploaded_file = st.file_uploader('Upload file')

    if uploaded_file is not None:
        # Check if the uploaded file is a .csv file
        if uploaded_file.type not in ['text/csv', 'text/plain']:
            st.error("Invalid format, please upload a .txt or .csv file")
            return
        # Display the file name if file is uploaded
        file_name = uploaded_file.name
        st.write("Your uploaded file name:", file_name)

        # Display the file contents
        file_content = uploaded_file.read()
        model_load = load_model(file_content, selected_option)
        
        st.write("Success!!!!!!! File contents:")
        st.write(model_load)

        st.session_state.uploaded_file = uploaded_file
        st.session_state.selected_option = selected_option
        st.session_state.model_load = model_load
    else:
        st.write("Please upload a file")

def tab2_solve_model():
    st.header("Tellurium/Roadrunner Modeling")
    st.subheader("Fill out information below to solve your model using tellurium")

    # Time inputs
    t0 = st.number_input("Enter your starting time: t0", value=0)
    tf = st.number_input("Enter your final time: tf", value=0)
    steps = st.number_input("Enter the number of steps you want", value=0)

    # Button to trigger processing
    if st.button("Solve Model"):
        if "model_load" in st.session_state:
            model_load = st.session_state.model_load
            #selected_option = st.session_state.selected_option
            try:
                #file_content = uploaded_file.read()
                #model_load = load_model(file_content, selected_option)
                df = simulate_model(model_load, t0, tf, steps)
                # returns result, df, species_names
                if "df" in st.session_state:
                    old_df = st.session_state.df
                    df = pd.concat([old_df, df], ignore_index=True)
                    
                st.write(df.head())
                st.session_state.df = df
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.write("Load model first")
    

    # Button to download the DataFrame as a CSV file
    if st.button("Download CSV"):
        # Create a link to download the CSV file
        if "df" in st.session_state:
            try:
                df = st.session_state.df
                csv = df.to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()  # Convert DataFrame to bytes
                href = f'<a href="data:file/csv;base64,{b64}" download="solved_model.csv">Download CSV File</a>'
                # ="solved_model:file/csv;base64,{b64}" download="solved_model.csv">Download CSV # File</a>'
                st.markdown(href, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.write("Load model first")


##### PLOTTING!!!!!!!!!!!!!!!!!!!
# Function to generate and display plot
def tab3_plot_all():
    st.header("Plotting All Data")
    if "df" in st.session_state:
        df = st.session_state.df
        try:
            fig = px.line(df, x=df.columns[0], y=df.columns[1:], title='Time Series Data')
            st.plotly_chart(fig)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.write("Load model first")

def tab4_plot_selected():
    st.header("Customizable Plot")
    if "df" in st.session_state:
        df = st.session_state.df
        # Display dropdown menu to choose X-axis 
        st.subheader("Select x-axis data:")
        x_column = st.selectbox('x-axis:', options=df.columns.tolist())

        # Display dropdown menu to choose Y-axis 
        st.subheader("Select Y axis data:")
        # User can select multiple species to plot
        y_columns = st.multiselect('Y axis:', options=df.columns.tolist())

        # Display input fields for user customization
        st.subheader("Plot Customization")
        title = st.text_input("Title", "Custom Plot")
        x_label = st.text_input("X-Axis Label", "X")
        y_label = st.text_input("Y-Axis Label", "Y")
     
        if y_columns:
            fig = px.line(df, x_column, y_columns)
            fig.update_layout(title=title, xaxis_title=x_label, yaxis_title=y_label)
            st.plotly_chart(fig)
        else:
            st.write('No Y columns selected.')
    else:
        st.write("Load model first")




### MAIN STREAMLIT APP CODE!!!!!!!!!!!!!!
def main():
    st.title('Compound Time Visualization')

    # Create tabs
    tabs = ["Upload model", "Solve model", "Plot all", "Plot selected"]
    selected_tab = st.sidebar.radio("Select Page", tabs)

    # Page 1 content
    if selected_tab == "Upload model": 
        tab1_upload_model()

    elif selected_tab == "Solve model":
        tab2_solve_model()

    elif selected_tab == "Plot all":
        tab3_plot_all()

    elif selected_tab == "Plot selected":
        tab4_plot_selected()
        

if __name__ == "__main__":
    main()
