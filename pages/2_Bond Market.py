import streamlit as st
import pandas as pd
import plotly.express as px
from pyecharts.charts import Line, Bar, Grid
from pyecharts import options as opts
from pyecharts.globals import ThemeType
from streamlit_echarts import st_pyecharts
from dataloader import yield_data

st.set_page_config(layout='wide')
rate_list,yield_list,tips_list = yield_data()


freq = rate_list['Frequency'].unique().tolist()
# #type = rates_df['Type'].unique().tolist()
# #var_names = rates_df['Name'].unique().tolist()

with st.sidebar:    
    freqency = st.radio('Select Frequency:', freq, horizontal=True)
    yield_list = yield_list[(yield_list['Frequency'] == freqency)]
    tips_list = tips_list[(tips_list['Frequency'] == freqency)]
    rate_list = rate_list[(rate_list['Frequency'] == freqency)]
    
    if freqency:
        display_col = ['Date','Name','Values']

        yield_list = yield_list[display_col]
        tips_list = tips_list[display_col]
        rate_list = rate_list[display_col]

# #---------------------------------------------------------------------------------

yield_name = yield_list['Name'].unique().tolist()
selection = st.multiselect('Select Tem Structure', yield_name, default = yield_name[0])
if selection:
    yield_df = yield_list[yield_list["Name"].isin(selection)]
    yield_df = yield_df.pivot(index = 'Date', columns = 'Name', values = 'Values').reset_index()
    yield_df = yield_df.fillna(method='ffill')

    def pct_change(df, date_col, value_cols):
        df_new = df[[date_col]].copy()
        for col in value_cols:
            df_new[col + '_change'] = df[col].diff()
        return df_new
    
    yield_change = pct_change(yield_df, 'Date', selection)


    # Function to create individual line charts for level
    def create_individual_line_chart(line, df):
        chart = (
            Line(init_opts=opts.InitOpts(height= '1000px',theme=ThemeType.LIGHT))
            .add_xaxis(df['Date'].tolist())
            .add_yaxis(line, df[line].tolist(),label_opts=opts.LabelOpts(is_show=False),symbol="none")
        )
        chart.set_global_opts(
            title_opts=opts.TitleOpts(),
            yaxis_opts=opts.AxisOpts(is_scale=True,type_='value',
                                     splitarea_opts=opts.SplitAreaOpts(
                is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=0.5))),
            xaxis_opts=opts.AxisOpts(is_scale=True,type_='time',boundary_gap=['0', '2%']),
            datazoom_opts=[opts.DataZoomOpts(is_show = True, type_="slider",range_start = 50,range_end = 100),
                           opts.DataZoomOpts(is_show = False, type_="inside")],
            tooltip_opts=opts.TooltipOpts(trigger="axis",axis_pointer_type="cross"),
            toolbox_opts = opts.ToolboxOpts(is_show=True),
        )
        return chart


col1,col2 = st.columns(2)
with col1:
     chart1 = None
     for line in selection:
        chart1 = create_individual_line_chart(line, yield_df)
        st_pyecharts(chart1)
     st.dataframe(yield_df, hide_index= True)
with col2:
     chart2 = None
     for line in selection:
            if line + '_change' in yield_change:
                chart2 = create_individual_line_chart(line + '_change', yield_change)
                st_pyecharts(chart2)
            else:
                st.write(f"No data available for {line} in the percentage change dataset.")
     st.dataframe(yield_change,hide_index= True)
# if chart1 and chart2:
#         st_pyecharts(chart1.overlap(chart2))
#-----------------------------------------------------------------------
st.divider()

tips_name = tips_list['Name'].unique().tolist()
selection = st.multiselect('Select Tem Structure', tips_name, default = '5-year')
if selection:
    tips_df = tips_list[tips_list["Name"].isin(selection)]
    tips_df = tips_df.pivot(index = 'Date', columns = 'Name', values = 'Values').reset_index()
    tips_df = tips_df.fillna(method='ffill')

def pct_change(df, date_col, value_cols):
    df_new = tips_df[['Date']].copy()
    for col in value_cols:
        df_new[col + '_change'] = df[col].diff()
    return df_new

tips_change = pct_change(tips_df,'Date', selection)

col1,col2 = st.columns(2)


with col1:
    st.dataframe(tips_df, hide_index= True)
with col2:
    st.dataframe(tips_change,hide_index= True)

#----------------------------------------------------------------------------
st.divider()

rate_name = rate_list['Name'].unique().tolist()
selection = st.multiselect('Select Tem Structure', rate_name, default = 'Bank prime loan')
if selection:
    rate_df = rate_list[rate_list["Name"].isin(selection)]
    rate_df = rate_df.pivot(index = 'Date', columns = 'Name', values = 'Values').reset_index()
    rate_df = rate_df.fillna(method='ffill')

def pct_change(df, date_col, value_cols):
    df_new = rate_df[['Date']].copy()
    for col in value_cols:
        df_new[col + '_change'] = df[col].diff()
    return df_new

rate_change = pct_change(rate_df,'Date', selection)

col1,col2 = st.columns(2)

with col1:
    st.dataframe(rate_df, hide_index= True)
with col2:
    st.dataframe(rate_change,hide_index= True)
