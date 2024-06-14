# import streamlit as st
# import streamlit_antd_components as sac
# import openpyxl
# import pandas as pd
# from dataloader import load_gdp_data
# from pyecharts.charts import Bar, Line
# from pyecharts import options as opts
# from streamlit_echarts import st_pyecharts
# from pyecharts.globals import ThemeType
# import plotly.express as px

# gdp_df, freq, type, unit, var_names = load_gdp_data()

# with st.sidebar:    
#     freqency = st.radio('Select Frequency:', freq, horizontal=True)
#     data_type = st.radio('Select Data Type:', type, horizontal=True)
#     unit_type = st.radio('Select Unit:', unit, horizontal=True)

#     gdp_df = gdp_df[(gdp_df['Frequency'] == freqency) &
#                     (gdp_df['Type'] == data_type) &
#                     (gdp_df['Unit'] == unit_type)       
#                     ]
#     if freqency == 'Quarterly':
#         gdp_df = gdp_df[['Date', 'Year_quarter','Name','Values']]
#     else:
#         gdp_df = gdp_df[['Date','Name','Values']]

#     st.divider()
#     st.subheader('Select Major Index:')

#     selected_names = []
#     for i, name in enumerate(var_names):
#         checkbox = st.checkbox(name,value=(i==0))
#         if checkbox:
#             selected_names.append(name)

# filtered_df = gdp_df[gdp_df["Name"].isin(selected_names)]
# if freqency == 'Quarterly':
#     final_df = filtered_df.pivot(index = ['Date','Year_quarter'], columns = ['Name'], values = 'Values').reset_index()
# else:
#     final_df = filtered_df.pivot(index = ['Date'], columns = ['Name'], values = 'Values').reset_index()

# if selected_names:
#     # Melt the DataFrame to long format for Plotly
#     df_melted = final_df.melt(id_vars='Date', value_vars=selected_names, var_name='Index Name:', value_name='Value')
#     fig = px.bar(df_melted, x='Date', y='Value', color='Index Name:', barmode='group', title='Dynamic Bar Chart')
#     st.plotly_chart(fig)
# else:
#     st.write("Please select at least one metric.")




# st.divider()

# st.dataframe(final_df,hide_index = True,column_order=('Date','Year_quarter','Gross domestic product','Personal consumption expenditures','Gross private domestic investment',
#                            'Government consumption expenditures and gross investment','Net exports of goods and services',
#                            'Exports','Imports','Residual'))




# # filtered_df = gdp_df[gdp_df["Name"].isin(selected_names)]
# # if freqency == 'Quarterly':
# #     final_df = filtered_df[['Date','Year_quarter','Name','Values']]
# # else:
# #     final_df = filtered_df[['Date','Name','Values']]