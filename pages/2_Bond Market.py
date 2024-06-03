import streamlit as st
import pandas as pd
import plotly.express as px
from pyecharts.charts import Line, Bar, Grid
from pyecharts import options as opts
from pyecharts.globals import ThemeType, JsCode
import plotly.graph_objects as go
from streamlit_echarts import st_pyecharts
from dataloader import yield_data

st.set_page_config(layout='wide')
rate_list,yield_list,tips_list = yield_data()
#--------------------------------------------------
# Term Structure Comparison:
display_col = ['Date','Name','Values']
st_order_col = ('Date','1-month','3-month','6-month','1-year','2-year','3-year','5-year','7-year','10-year','20-year','30-year')
order_col = ['1-month','3-month','6-month','1-year','2-year','3-year','5-year','7-year','10-year','20-year','30-year']
tips_col = ['5-year','7-year','10-year','20-year','30-year']
term_yield_list = yield_list[(yield_list['Frequency'] == 'Weekly')]
term_tips_list = tips_list[(tips_list['Frequency'] == 'Weekly')]
term_yield_list = term_yield_list[display_col]
term_tips_list = term_tips_list[display_col]

# term structure for yield maturity
term_yield_df = term_yield_list.pivot(index = 'Date', columns = 'Name', values = 'Values')
term_yield_df = term_yield_df.sort_values(by ='Date',ascending=False)
term_yield_df = term_yield_df.drop('Federal funds (effective)', axis=1).dropna()
term_yield_df = term_yield_df[order_col]

# term structure for TIPS (real rates)
term_tips_df = term_tips_list.pivot(index = 'Date', columns = 'Name', values = 'Values')
term_tips_df = term_tips_df.sort_values(by ='Date',ascending=False)
term_tips_df = term_tips_df[tips_col]

# Initialize session state
if 'row_index1' not in st.session_state:
    st.session_state.row_index1 = 0
if 'row_index2' not in st.session_state:
    st.session_state.row_index2 = 1

def display_rows(row_index1, row_index2):
    st.write("Row 1:")
    st.dataframe(term_yield_df.iloc[[row_index1]])
    st.write("Row 2:")
    st.dataframe(term_yield_df.iloc[[row_index2]])

    # Create a line chart for the two selected rows
    sorted_df = term_yield_df.iloc[[row_index1, row_index2]].T
    fig = px.line(sorted_df)
    fig.data[0].line.color = 'darkgreen'
    fig.data[1].line.color = 'darkorange'
    for column in sorted_df.columns:
        for i, value in enumerate(sorted_df[column]):
            fig.add_annotation(x=sorted_df.index[i], y=value, text=str(value),
                               showarrow=False, font=dict(color='black'),yshift=10)
    # Add scatter plot with markers
    fig.add_trace(go.Scatter(
        x=sorted_df.index,
        y=sorted_df.iloc[:, 0],  # Taking values from the first selected row
        mode='markers',
        marker=dict(color='green'),
        showlegend=False  # Color for the first row's markers
    ))
    fig.add_trace(go.Scatter(
        x=sorted_df.index,
        y=sorted_df.iloc[:, 1],  # Taking values from the second selected row
        mode='markers',
        marker=dict(color='orange'),
        showlegend=False,  # Color for the second row's markers
    ))
    fig.update_layout(
        title=f"Interest Rates for {term_yield_df.index[row_index1]} and {term_yield_df.index[row_index2]}",
        xaxis_title="Maturity",
        yaxis_title="Interest Rate (%)",
        yaxis_range=[3, max(sorted_df.max()) * 1.2],
        xaxis=dict(linecolor='black', linewidth=1), 
        yaxis=dict(linecolor='black', linewidth=1,dtick=0.5),
        autosize=True,
        xaxis_range=[term_yield_df.index.min(), term_yield_df.index.max()],

    )
    st.plotly_chart(fig, use_container_width=True,config={"scrollZoom": True})

# Button to go to the previous row for the first index
if st.button('Previous Week'):
    if st.session_state.row_index1 > 0:
        st.session_state.row_index1 -= 1

# Button to go to the next row for the first index
if st.button('Next week'):
    if st.session_state.row_index1 < len(term_yield_df) - 1:
        st.session_state.row_index1 += 1

if st.button('Previous Row 2'):
    if st.session_state.row_index2 > 0:
        st.session_state.row_index2 -= 1

# Button to go to the next row for the second index
if st.button('Next Row 2'):
    if st.session_state.row_index2 < len((term_yield_df)) - 1:
        st.session_state.row_index2 += 1

if st.session_state.row_index2 <= st.session_state.row_index1:
    st.session_state.row_index2 = st.session_state.row_index1 + 1

display_rows(st.session_state.row_index1,st.session_state.row_index2)

st.divider()

st.dataframe(term_yield_df, column_order= st_order_col)

st.divider()
#----------------------------------------------------------------------
def display_rows(row_index1, row_index2):
    st.write("Row 1:")
    st.dataframe(term_tips_df.iloc[[row_index1]])
    st.write("Row 2:")
    st.dataframe(term_tips_df.iloc[[row_index2]])

    # Create a line chart for the two selected rows
    sorted_df = term_tips_df.iloc[[row_index1, row_index2]].T
    fig = px.line(sorted_df)
    fig.data[0].line.color = 'darkgreen'
    fig.data[1].line.color = 'darkorange'
    for column in sorted_df.columns:
        for i, value in enumerate(sorted_df[column]):
            fig.add_annotation(x=sorted_df.index[i], y=value, text=str(value),
                               showarrow=False, font=dict(color='black'),yshift=10)
    # Add scatter plot with markers
    fig.add_trace(go.Scatter(
        x=sorted_df.index,
        y=sorted_df.iloc[:, 0],  # Taking values from the first selected row
        mode='markers',
        marker=dict(color='green'),
        showlegend=False  # Color for the first row's markers
    ))
    fig.add_trace(go.Scatter(
        x=sorted_df.index,
        y=sorted_df.iloc[:, 1],  # Taking values from the second selected row
        mode='markers',
        marker=dict(color='orange'),
        showlegend=False,  # Color for the second row's markers
    ))
    fig.update_layout(
        title=f"Interest Rates for {term_yield_df.index[row_index1]} and {term_yield_df.index[row_index2]}",
        xaxis_title="Maturity",
        yaxis_title="Interest Rate (%)",
        yaxis_range=[1.5, max(sorted_df.max()) * 1.2],
        xaxis=dict(linecolor='black', linewidth=1), 
        yaxis=dict(linecolor='black', linewidth=1,dtick=0.2),
        autosize=True,
        xaxis_range=[term_yield_df.index.min(), term_yield_df.index.max()],

    )
    st.plotly_chart(fig, use_container_width=True,config={"scrollZoom": True})
display_rows(st.session_state.row_index1,st.session_state.row_index2)
st.dataframe(term_tips_df, column_order= st_order_col)

st.divider()
#----------------------------------------------------------------------
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
            .add_yaxis(line, df[line].tolist(),linestyle_opts=opts.LineStyleOpts(width=1.5),
                       label_opts=opts.LabelOpts(is_show=False),symbol="none")
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
