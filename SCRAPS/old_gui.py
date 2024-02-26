import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

### FUNCTIONS!!!!!!!!!11
# Function to read and display CSV file
def read_csv(file):
    try: 
        df = pd.read_csv(file)
        return df
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Function to generate plot
def visualize_data(df):
    try:
        fig = px.line(df, x=df.columns[0], y=df.columns[1:], title='Time Series Data')
        st.plotly_chart(fig)
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Function to generate plot with selected columns
def generate_plot(df, x_column, y_columns):
    fig = go.Figure()
    for y_column in y_columns:
        fig.add_trace(go.Scatter(x=df[x_column], y=df[y_column], mode='lines', name=y_column))
    fig.update_layout(title='Customizable Plot', xaxis_title=x_column, yaxis_title='Value')
    return fig


### MAIN STREAMLIT APP CODE!!!!!!!!!!!!!!
def main():
    st.title('Compound Time Visualization')

    # Upload CSV file
    file = st.file_uploader('Upload CSV', type=['csv'])
    
    if file is not None:
        df = read_csv(file)
        if df is not None:
            # Display first few rows of the data
            st.write("Data Preview:")
            st.write(df.head())
            
            # Visualize data
            visualize_data(df)

            # Button to create second plot
            if st.button('Plot selected columns:'):
                st.title('Customizable Plot')
                # Display available columns and checkboxes
                st.write('### Select Columns:')
                columns = df.columns[1:].tolist()
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



if __name__ == "__main__":
    main()
