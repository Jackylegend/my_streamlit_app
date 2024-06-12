import streamlit as st
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
from streamlit_navigation_bar import st_navbar

st.set_page_config(layout='wide')
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

                base = alt.Chart(fed_df).encode(
                    x='Date:T'
                )

                line_chart = base.mark_line(color='blue').encode(
                    y=alt.Y(name, axis=alt.Axis(title=name)),
                    tooltip=['Date', name]
                ).properties(
                    title=f'{name} - {type} - {freq}'
                )

                diff_chart = base.mark_line(color='red').encode(
                    y=alt.Y('Daily_Change', axis=alt.Axis(title=f'Daily Difference of {name}')),
                    tooltip=['Date', 'Daily_Change']
                ).properties(
                    title=f'Daily Difference of {name} - {type} - {freq}'
                )

                combined_chart = alt.vconcat(
                    line_chart, diff_chart
                ).resolve_scale(
                    y='independent'
                ).properties(
                ).interactive()
                st.altair_chart(combined_chart, use_container_width=True)

    other_names = [name for name in selected_names if name != 'Fed Fund Rate']
    for name in other_names:
        other_df = filtered_df[['Date', name]].dropna(subset=[name])
        
        other_chart = alt.Chart(other_df).mark_line().encode(
            x='Date:T',
            y=alt.Y(name, title=name),
            tooltip=['Date', name]
        ).interactive().properties(
            title=f'{name} - {type} - {freq}'
        )

        st.altair_chart(other_chart, use_container_width=True)
















    st.dataframe(filtered_df, hide_index=True,column_order= st_order_col, use_container_width=True)
else:
    st.write("No data to display with the selected filters.")






# if not filtered_df.empty:
#     filtered_df = filtered_df[['Date', 'Name', 'Values']]
#     filtered_df = filtered_df.pivot_table(index='Date', columns='Name', values='Values').reset_index()

#     # Separate Plotly Express line plots for different groups of names
#     if 'Fed Fund Rate' in selected_names:
#         for name in selected_names:
#             if name == 'Fed Fund Rate':
#                 fed_df = filtered_df[['Date', name]].dropna()
#                 diff_name = f'Daily Difference of {name}'
#                 fed_df['Daily_Change'] = fed_df[name].diff()

#                 fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=[name, diff_name])
#                 fig.add_trace(go.Scatter(x=fed_df['Date'], y=fed_df[name], mode='lines', name=name),row=1,col=1)
#                 fig.add_trace(go.Scatter(x=fed_df['Date'], y=fed_df['Daily_Change'], mode='line', name=diff_name),row=2,col=1)
#                 fig.update_layout(height=800,title=f'{name} and Daily Difference - {type} - {freq}',
                
#             )
# #yaxis=dict(title=name), yaxis2=dict(title=diff_name, overlaying='y', side='right')
#                 #fig_fed_fund = px.line(fed_df, x='Date', y=name, title=f'{name} - {type} - {freq}')
#                 st.plotly_chart(fig)
    
#     other_names = [name for name in selected_names if name != 'Fed Fund Rate']
#     for name in other_names:
#         other_df = filtered_df[['Date', name]].dropna(subset=[name])
#         fig_other = px.line(other_df, x='Date', y=name, title=f'{name} - {type} - {freq}')
#         st.plotly_chart(fig_other)