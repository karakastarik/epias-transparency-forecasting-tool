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
st.write("""
## Forecasting Tool# 
# """)

#st.table(mcp_data.head())
#st.write("""## Consumption""")
#st.table(consumption_data.head())
#st.write("""## Real Time Generation Data""")
#st.table(real_time_gen_data.head())
#st.line_chart(consumption_data.Consumption)

st.subheader("Hourly Consumption (MWh)")
fig_cons = go.Figure()
fig_cons.add_trace(go.Scatter(x=consumption_data.Date, y=consumption_data.Consumption, mode='lines',name='Consumption (MWh)'))
fig_cons.update_layout(xaxis_title='Date',yaxis_title='Consumption (MWh)',plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig_cons)

st.subheader("Market Clearing Price-TL")
fig_mcp = go.Figure()
fig_mcp.add_trace(go.Scatter(x=mcp_data.Date, y=mcp_data.MCP_TL, mode='lines',name='MCP TL'))
fig_mcp.update_layout(xaxis_title='Date',yaxis_title='MCP',plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig_mcp)

#fig = px.line(data, x=~Date,y = ~Consumption,name = "Consumption", type = 'scatter', mode = 'lines') 
#fig = fig.add_trace(data,y = ~Generation , name = 'Generation', mode = 'lines') 

