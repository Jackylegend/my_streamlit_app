import streamlit as st
import streamlit_antd_components as sac
from dataloader import load_gdp_data
from pyecharts.charts import Bar, Line

def app():
    gdp_df, freq, type, unit = load_gdp_data()

    with st.sidebar:
        select_freq = st.radio('Select Frequency Type:',freq)
        select_type = st.radio('Select GDP Type:',type)
        select_unit = st.radio('Select Units:',unit)

        sac.menu([sac.MenuItem(type='divider')])

        index_select = sac.tree(items=[
            sac.TreeItem('Gross Domestic Product',icon='apple',children=[
                sac.TreeItem('Personal Consumption Expenditures',icon='apple'),
                sac.TreeItem('Private Domestic Investment',icon='apple'),
                sac.TreeItem('Government Consumption Expenditures and Investment',icon='apple'),
                sac.TreeItem('Exports',icon='apple'),
                sac.TreeItem('Imports',icon='apple')]),
                ], label='Index Level',index=0, size='md', icon='table', open_all=True, checkbox=True, checkbox_strict=True)
            
        sac.menu([sac.MenuItem(type='divider')],key= 'divider')

        compo_select = sac.tree(items=[
             sac.TreeItem('Personal Consumption Expenditures',icon='apple'),
             sac.TreeItem('Private Domestic Investment',icon='apple'),
             sac.TreeItem('Government Consumption Expenditures and Investment',icon='apple'),
             sac.TreeItem('Exports',icon='apple'),
             sac.TreeItem('Imports',icon='apple')
        ], key= 'subcomponent', label='Sub-Components Level', size='md', icon='table', open_all=False, checkbox=True)


# #---------------------------------------------------------------------------    
#     if select_type == 'Real GDP':
#         table['Type'].unique() == 'Real'
#     else:
#         table['Type'].unique() == 'Nonimal'
# #---------------------------------------------------------------------------      
#     if select_unit == '%':
#         table['Unit'] == 'Pct'
#     else:
#         table['Unit'] == 'Dollar in Billions'
# #---------------------------------------------------------------------------  
#     if index_select == 'Gross Domestic Product':
#         table['Index_Level'] == 0
#     elif index_select == 'Personal Consumption Expenditures':
#         table['Index_Level'] == 1 & table['Name'] == 'Personal consumption expenditures'
#     elif index_select == 'Private Domestic Investment':
#         table['Index_Level'] = 1 & table['Name'] == 'Gross private domestic investment'
#     elif index_select == 'Government Consumption Expenditures and Investment':
#         table['Index_Level'] = 1 & table['Name'] == 'Government consumption expenditures and gross investment'
#     elif index_select == 'Exports':
#         table['Index_Level'] = 1 & table['Name'] == 'Exports'
#     elif index_select == 'Imports':
#         table['Index_Level'] = 1 & table['Name'] == 'Imports'
    

    col1, col2, col3 = st.columns(3)
    # Filter based on select_type, select_unit, and index_select
    
    table = gdp_df[(gdp_df['Frequency'] == select_freq) &
                   (gdp_df['Type'] == select_type) &
                   (gdp_df['Unit'] == select_unit)
                   
                   ]
    
    if select_freq == 'Quarterly':
        selected_columns = ['Date','Year_quarter','Name','Values']
    else:
        selected_columns = ['Date','Name','Values']
   
#     table = table[
#         (table['Type'] == 'Real' if select_type == 'Real GDP' else table['Type'] == 'Nominal') &
#         (table['Unit'] == 'Pct' if select_unit == '%' else table['Unit'] == 'Dollar in Billions') &
#         (
#             (table['Index_Level'] == 0) |
#             (
#                 (table['Index_Level'] == 1) &
#                 (
#                     (table['Name'] == 'Gross Domestic Product' if index_select == 'Gross Domestic Product' else False) |
#                     (table['Name'] == 'Personal consumption expenditures' if index_select == 'Personal Consumption Expenditures' else False) |
#                     (table['Name'] == 'Gross private domestic investment' if index_select == 'Private Domestic Investment' else False) |
#                     (table['Name'] == 'Government consumption expenditures and gross investment' if index_select == 'Government Consumption Expenditures and Investment' else False) |
#                     (table['Name'] == 'Exports' if index_select == 'Exports' else False) |
#                     (table['Name'] == 'Imports' if index_select == 'Imports' else False)
#                 )
#             )
#         )
#     ]

# # Select specific columns based on filtered DataFrame's columns
#     selected_cols = st.multiselect('Select Columns', table.columns)

# Display the selected columns from the filtered DataFrame
    st.dataframe(table[selected_columns])


    # selection = [select_type,select_unit,index_select]
    # st.dataframe(table[selection])

    st.divider()



    
# #---------------------------------------------------------------------------  
#     # charting / dataframe dataset
#     # mapping_table = table[(select2) & (select3) & (index_select)]

    st.write("Hello World - this is gdp page")