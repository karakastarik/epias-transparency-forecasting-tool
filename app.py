import functions as func # import functions.py file
import streamlit as st #streamlit
import datetime 
from datetime import timedelta 
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go

start_date=st.sidebar.date_input(label="Start Date", value=datetime.date.today()-datetime.timedelta(days=1))
end_date=st.sidebar.date_input("End Date", value=datetime.date.today())

#PTF
mcp_data = func.mcp(startDate=str(start_date),endDate=str(end_date))
mcp_data.head()
#Consumption
consumption_data = func.consumption_realtime(startDate=str(start_date),endDate=str(end_date))
consumption_data.head()
#Real time generation
real_time_gen_data = func.real_time_gen(startDate=str(start_date),endDate=str(end_date))
real_time_gen_data.head()

#Stremlit Side
st.markdown("<h1 style='text-align: center; color: black;'>Forecasting Tool</h1>", unsafe_allow_html=True)
cons_describe=pd.DataFrame(consumption_data.describe()).reset_index().rename(index=str,columns={"index":"Statistic"})

st.markdown("<h3 style='text-align: center; color: black;'>Consumption-Descriptive Statistics</h3>", unsafe_allow_html=True)
st.table(cons_describe)
#st.table(pd.DataFrame(consumption_data.describe()).reset_index().rename(index=str,columns={"index":"Statistic"}))
#cons_table = go.Figure(data=[go.Table(
#    header=dict(values=list(cons_describe.columns),
#                fill_color='midnightblue',
#                align='center'),
#    cells=dict(values=[cons_describe.Statistic, cons_describe.Consumption],
#               fill_color='lightgrey',
#               align='center'))
#])

#st.plotly_chart(cons_table)
st.markdown("<h3 style='text-align: center; color: black;'>Hourly Consumption (MWh)</h3>", unsafe_allow_html=True)
#cons_markdown = f"Average hourly consumption in the last **{consumption_data.Date.count()}** hours is: **{consumption_data.Consumption.mean():.2f}**."
#st.markdown(cons_markdown)
fig_cons = go.Figure()
fig_cons.add_trace(go.Scatter(x=consumption_data.Date, y=consumption_data.Consumption, mode='lines',name='Consumption (MWh)'))
fig_cons.update_layout(xaxis_title='Date',yaxis_title='Consumption (MWh)',plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig_cons)

st.markdown("<h3 style='text-align: center; color: black;'>Market Clearing Price-Descriptive Statistics</h3>", unsafe_allow_html=True)
st.table(pd.DataFrame(mcp_data.describe()).reset_index().rename(index=str,columns={"index":"Statistic"}))
st.markdown("<h3 style='text-align: center; color: black;'>Market Clearing Price-TL</h3>", unsafe_allow_html=True)
fig_mcp = go.Figure()
fig_mcp.add_trace(go.Scatter(x=mcp_data.Date, y=mcp_data.MCP_TL, mode='lines',name='MCP TL'))
fig_mcp.update_layout(xaxis_title='Date',yaxis_title='MCP',plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig_mcp)

#fig = px.line(data, x=~Date,y = ~Consumption,name = "Consumption", type = 'scatter', mode = 'lines') 
#fig = fig.add_trace(data,y = ~Generation , name = 'Generation', mode = 'lines') 

