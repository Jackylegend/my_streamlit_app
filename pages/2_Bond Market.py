import streamlit as st
import pandas as pd
import plotly.express as px
from dataloader import yield_data

rates_df, freq, type, var_names = yield_data()

with st.sidebar:    
    freqency = st.radio('Select Frequency:', freq, horizontal=True)
    data_type = st.radio('Select Data Type:', type, horizontal=True)

    rates_df = rates_df[(rates_df['Frequency'] == freqency) &
                    (rates_df['Type'] == data_type)
                ]
    
    rates_df = rates_df[['Date','Name','Values']]
    st.divider()
    st.subheader('Select Major Index:')

    selected_names = []
    for i, name in enumerate(var_names):
        checkbox = st.checkbox(name,value=(i==0))
        if checkbox:
            selected_names.append(name)

filtered_df = rates_df[rates_df["Name"].isin(selected_names)]

final_df = filtered_df.pivot(index = 'Date', columns = 'Name', values = 'Values').reset_index()

if selected_names:
    # Melt the DataFrame to long format for Plotly
    df_melted = final_df.melt(id_vars='Date', value_vars=selected_names, var_name='Index Name:', value_name='Value')
    fig = px.line(df_melted, x='Date', y='Value', color='Index Name:', title='Dynamic Bar Chart')
    st.plotly_chart(fig)
else:
    st.write("Please select at least one metric.")