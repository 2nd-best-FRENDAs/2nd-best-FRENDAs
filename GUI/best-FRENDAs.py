import streamlit as st

import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objs as go
import tellurium as te
import numpy as np
import base64

from functions_to_import import load_model, simulate_model, titration_plot

### FUNCTIONS!!!!!!!!!
def tab1_upload_model():
    """ 
    First tab in GUI, where user uploads there file and selects file format.
    Outputs a roadrunner/tellurium model stored in session state.
    """
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

        # Stores model in session state of GUI, as well as uploaded file and selection choice
        st.session_state.uploaded_file = uploaded_file
        st.session_state.selected_option = selected_option
        st.session_state.model_load = model_load
    else:
        # If no file uploaded
        st.write("Please upload a file")

def tab2_solve_model():
    """
    Second tab of GUI used to solve ODEs and simulate the model.
    Time interval inputted by the user. 
    
    Outputs a dataframe with concentrations over interval of time.
    User able to download and save the dataframe as .csv 
    """    
    # Enable user-define time inputs
    t0 = st.number_input("Enter your starting time: t0", value=0)
    tf = st.number_input("Enter your final time: tf", value=0)
    steps = st.number_input("Enter the number of steps you want", value=0)
    
    # Button to trigger processing
    solve_button = st.button("Solve Model")
    if 'solve_button' not in st.session_state:
        st.session_state.solve_button = False

    # Initializing variables
    if 't0' not in st.session_state:
        st.session_state.t0 = 0
    if 'tf' not in st.session_state:
        st.session_state.tf = 0
    if 'steps' not in st.session_state:
        st.session_state.steps = 0
        
    # Check if any of the input variables has changed
    if (st.session_state.t0 != t0 or st.session_state.tf != tf or st.session_state.steps != steps):
        st.session_state.solve_button = False
        #WHY IS THIS NOT WORKING??????????
        df = None
        st.session_state.pop('df', None)

    if solve_button:
        if not st.session_state.solve_button:
            st.session_state.solve_button = True
            # Store the current input variables in session state
            st.session_state.t0 = t0
            st.session_state.tf = tf
            st.session_state.steps = steps
            if "model_load" in st.session_state:
                try:
                    df = simulate_model(st.session_state.model_load, t0, tf, steps)
                    st.write(df)
                    st.session_state.df = df
                except Exception as e:
                    st.error(f"An error occurred: {e}")
            else:
                st.write("Load model first")
        else:
            st.write(st.session_state.df)
            st.write("model already solved!")
    

    # Button to download the DataFrame as a CSV file
    if st.button("Download CSV"):
        # Create a link to download the CSV file
        if "df" in st.session_state:
            try:
                df = st.session_state.df
                csv = df.to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()  # Convert DataFrame to bytes
                href = f'<a href="data:file/csv;base64,{b64}" download="solved_model.csv">Download CSV File</a>'
                st.markdown(href, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.write("Load model first")


##### PLOTTING!!!!!!!!!!!!!!!!!!!
# Function to generate and display plot
def tab3_plot_all():
    """
    Third tab to display plot of every component concentration against time
    Takes output dataframe, stored in session state, and plots concentration.
    """
    st.header("Plotting All Data")
    st.write("Below is your plot of all metabolite and enzyme concentrations (in mM) against your specified time interval (in seconds).")
    if "df" in st.session_state:
        df = st.session_state.df
        try:
            fig = px.line(df, x=df.columns[0], y=df.columns[1:], title='Time Series Data')
            fig.update_layout(xaxis_title="Time (seconds)", yaxis_title="Concentration (mM)")
            st.plotly_chart(fig)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.write("Load model first")

def tab4_plot_selected():
    """
    Fourth tab where the user chooses what components to plot against time.
    User defines plot title, and x- and y-labels.
    """
    st.header("Customizable Plot")
    st.write("Please fill out information below. Then, a specified plot of metabolite and enzyme concentrations (in mM) against your specified time interval (in seconds) will appear.")
    st.divider()
    if "df" in st.session_state:
        df = st.session_state.df
        # Display dropdown menu to choose X-axis 
        st.subheader("Select X-axis data:")
        st.write("Only able to select one column from dataframe.")
        x_column = st.selectbox('X-axis:', options=df.columns.tolist())

        # Display dropdown menu to choose Y-axis 
        st.subheader("Select Y-axis data:")
        st.write("Able to select many columns from dataframe.")
        # User can select multiple species to plot
        y_columns = st.multiselect('Y-axis:', options=df.columns.tolist())

        # Display input fields for user customization
        st.subheader("Plot Formatting & Customization")
        st.write("Define plot title, and X- and Y-labels.")
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

def tab5_plot_foldchange():
    st.header("Plot species with selected fold change")
    st.write("Please fill out information below. Then, a specified plot species with a fold change greater than specified will appear.")
    st.divider()
    if "df" in st.session_state:
        df = st.session_state.df
        t0 = st.session_state.t0
        tf = st.session_state.tf
        input_foldchange = st.number_input("Enter the foldchange you would like to filter for", value=0)
        # Button to trigger processing
        plot_foldchange = st.button("Plot species with fold change x")
        if plot_foldchange:
            filtered_columns = []
            for column in df.columns[1:]:
                initial_value = df[column].iloc[t0]
                final_value = df[column].iloc[tf]
                min_value = min(initial_value, final_value)
                max_value = max(initial_value, final_value)
                if abs(max_value - min_value) > input_foldchange * min_value:
                    filtered_columns.append(column)
            st.write(df[filtered_columns])
            fig = px.line(df, 'Time', filtered_columns)
            fig.update_layout(title=f"Plot of species with fold change greater than {input_foldchange}",xaxis_title='Time', yaxis_title='Concentration (uM)')
            st.plotly_chart(fig)
    else:
        st.write("Load model first")


def tab6_plot_titration():
    st.header("Titration Plot")
    st.write("Please fill out information below. The button will rerun solving the model for varying concentration ranges of the species selected and show a plot.")
    st.divider()
    if "df" in st.session_state and "uploaded_file" in st.session_state:
        df = st.session_state.df
        uploaded_file = st.session_state.uploaded_file
        model_load = st.session_state.model_load
        selected_option = st.session_state.selected_option
        t0 = st.session_state.t0
        tf = st.session_state.tf
        steps = st.session_state.steps
        #user select which species to vary
        species = st.selectbox('Species to titrate:', options=df.columns[1:].tolist())
        titration_conc = st.number_input("Enter the range of titrations you want, 0 to this value (in steps of 1)", value=0)
        init_conc = df[species].iloc[t0]
        st.write(f"The initial concentration of {species} was {init_conc}")

        # Button to trigger processing
        plot_titration = st.button("Plot titration")
        if plot_titration:
            file_name = uploaded_file.name
            titration_df = titration_plot(uploaded_file, species, titration_conc, t0, tf, steps, selected_option)
            st.write(titration_df)
    
            # Get the names of species for the legend
            headings = titration_df.columns[1:]
            # Create figure with Plotly Express
            fig = px.line(titration_df, x='Time', y=headings, title=species + ' Titration')
            # Update axis labels
            fig.update_xaxes(title_text='Time (s)')
            fig.update_yaxes(title_text='Concentration (uM)')
            st.plotly_chart(fig)
    else:
        st.write("Load model first")



### MAIN STREAMLIT APP CODE!!!!!!!!!!!!!!

def main():
    st.title('Compound Time Visualization')

    # Create tabs
    tab1, tab2, tab3 = st.tabs(["🗃 Upload model", "🗃 Solve model", "📈 Plotting"])

    # Tab 1: uploading model
    with tab1:
        st.subheader("Upload your file here")
        st.write("The file should be in antimony or SBML format. Please select file format from the dropdown below before solving the model.")
        st.divider()
        tab1_upload_model()

    # Tab 2: Solving model
    with tab2:
        st.subheader("Tellurium/Roadrunner Modeling")
        st.write("Please input the time interval for your simulation. Specify how many time points used in the interval to simulate your model.")
        st.divider()
        tab2_solve_model()

    # Tab 3: Plotting model
    with tab3:
        st.header("Plotting simulation results")
        st.write("To visualize your results, the Plot all tab will show the changing concentrations (in mM) of all compounds against time (in seconds). The second tab, Plot Selected, allows you to select your X- and Y-axis contents, and define a plot title and labels. Each plot can be downloaded and saved as a PNG file.")
        st.divider()
        sub_tabs = ["Plot all", "Plot selected", "Plot fold change", "Plot titration"]
        with st.expander("Select Page"):
            selected_sub_tab = st.radio("", sub_tabs, index=0)
            if selected_sub_tab == "Plot all": 
                tab3_plot_all()
            elif selected_sub_tab == "Plot selected":
                tab4_plot_selected()
            elif selected_sub_tab == "Plot fold change":
                tab5_plot_foldchange()
            elif selected_sub_tab == "Plot titration":
                tab6_plot_titration()

if __name__ == "__main__":
    main()
