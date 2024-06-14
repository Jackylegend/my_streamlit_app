import streamlit as st
import streamlit_antd_components as sac
import pandas as pd
import plotly.express as px
from pyecharts.charts import Line, Bar, Grid
from pyecharts import options as opts
from pyecharts.globals import ThemeType, JsCode
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from streamlit_echarts import st_pyecharts
from dataloader import yield_data
import altair as alt

def app():
    rate_list,data_type,tips_list, rates_df = yield_data()

    # List of freqency, types, names
    frequency = rate_list
    type = data_type


    #name_opts = ['Fed Fund Rate','1-month','3-month','6-month','1-year','2-year','3-year','5-year','7-year','10-year','20-year','30-year']
    st_order_col = ('Date','Fed Fund Rate','1-month','3-month','6-month','1-year','2-year','3-year','5-year','7-year','10-year','20-year','30-year')

    col1, col2 = st.columns(2,gap="small")

    with col1:
        freq = st.radio('Select Frequency:', frequency, horizontal=True)
    with col2:
        type = st.radio("Data Type", type, horizontal=True)

    name = rates_df[(rates_df['Frequency'] == freq) & (rates_df['Type'] == type)]
    name_opts = name['Name'].unique()

    selected_names = []
    st.markdown("Select Name:")
    cols = st.columns(len(name_opts),gap='small')
    for col, name in zip(cols, name_opts):
        if col.checkbox(name, key=name):
            selected_names.append(name)
                
    filtered_df = rates_df[(rates_df['Frequency'] == freq) & 
                            (rates_df['Type'] == type) &
                            (rates_df['Name'].isin(selected_names))
                            ]


    # Display filtered DataFrame and plots
    if not filtered_df.empty:
        filtered_df = filtered_df[['Date', 'Name', 'Values']]
        filtered_df = filtered_df.pivot_table(index='Date', columns='Name', values='Values').reset_index()

        # Separate Altair line plots for different groups of names
        if 'Fed Fund Rate' in selected_names:
            for name in selected_names:
                if name == 'Fed Fund Rate':
                    fed_df = filtered_df[['Date', name]].dropna()
                    fed_df['Daily_Change'] = fed_df[name].diff()

                    st.line_chart(fed_df,x= 'Date',y = name, use_container_width=True)

        other_names = [name for name in selected_names if name != 'Fed Fund Rate']
        for name in other_names:
            other_df = filtered_df[['Date', name]].dropna(subset=[name])

            st.bar_chart(other_df,x='Date',y='name', use_container_width=True)