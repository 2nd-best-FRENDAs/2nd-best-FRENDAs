import streamlit as st
import pandas as pd
import plotly.graph_objs as go

# Sample DataFrame
data = {
    'x': [1, 2, 3, 4, 5],
    'y1': [10, 15, 13, 18, 20],
    'y2': [5, 8, 9, 7, 11],
    'y3': [12, 9, 11, 14, 10]
}
df = pd.DataFrame(data)

# Function to generate plot with selected columns
def generate_plot(df, x_column, y_columns):
    fig = go.Figure()
    for y_column in y_columns:
        fig.add_trace(go.Scatter(x=df[x_column], y=df[y_column], mode='lines', name=y_column))
    fig.update_layout(title='Customizable Plot', xaxis_title=x_column, yaxis_title='Value')
    return fig

# Streamlit app
def main():
    st.title('Customizable Plot')

    # Display available columns and checkboxes
    st.write('### Select Columns:')
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

if __name__ == "__main__":
    main()
