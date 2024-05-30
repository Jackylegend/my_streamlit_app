import streamlit as st
import openpyxl
import pandas as pd

#---------------------------------------------------------------------------------------------------------------------------------------

# Loading GDP data
@st.cache_data
def load_gdp_data():
    gdp_df = pd.read_excel('dataset/gdp.xlsx')
    gdp_df = gdp_df[(gdp_df['Index_Level'] == 0) | (gdp_df['Index_Level'] == 1)]
    gdp_df['Date'] = pd.to_datetime(gdp_df['Date']).dt.strftime('%Y-%m-%d')
    freq = gdp_df['Frequency'].unique().tolist()
    type = gdp_df['Type'].unique().tolist()
    unit = gdp_df['Unit'].unique().tolist()
    var_names = gdp_df['Name'].unique().tolist()
    return gdp_df, freq, type, unit, var_names


#---------------------------------------------------------------------------------------------------------------------------------------

# Loading IR data
# @st.cache
# def yield_data():
#     # Load your dataset here
#     data = pd.read_csv('path/to/your/dataset.csv')
#     return data


