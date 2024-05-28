import streamlit as st
import openpyxl
import pandas as pd

#---------------------------------------------------------------------------------------------------------------------------------------

# Loading GDP data
@st.cache_data
def load_gdp_data():
    gdp_df = pd.read_excel('dataset/gdp.xlsx')

    gdp_df['Date'] = pd.to_datetime(gdp_df['Date']).dt.strftime('%m-%d-%Y')

    freq = gdp_df['Frequency'].unique().tolist()
    type = gdp_df['Type'].unique().tolist()
    unit = gdp_df['Unit'].unique().tolist()




    # Filter Variables
    # index_level = gdp['Index_Level'].unique()
    # index_mapping = gdp.loc[gdp['Index_Level'].isin(index_level), ['Index_Mapping']]
    # parent_level = gdp['Index_Mapping'].unique()
    # type_ = gdp['Type'].unique()
    # freq = gdp['Frequency'].unique()
    # unit = gdp['Unit'].unique()
    # data_col =['DATE','Name','real_pct_Quarter','nominal_GDP_Quarter','nominal_pct_Quarter','real_GDP_Quarter','nominal_GDP_Annual','nominal_pct_Annual','real_GDP_Annual','real_pct_Annual']
    return gdp_df, freq, type, unit

#---------------------------------------------------------------------------------------------------------------------------------------

# Loading IR data
# @st.cache
# def yield_data():
#     # Load your dataset here
#     data = pd.read_csv('path/to/your/dataset.csv')
#     return data


