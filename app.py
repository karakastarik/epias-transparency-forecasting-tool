import functions as func # import functions.py file
import streamlit as st #streamlit
import time
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
# Forecasting Tool# 
# """)

st.write("""## MCP""")
st.write(mcp_data.head())
st.write("""## Consumption""")
st.write(consumption_data.head())
st.write("""## Real Time Generation Data""")
st.write(real_time_gen_data.head())
st.line_chart(consumption_data.Consumption)

#fig = go.Figure()
#fig.add_trace(go.Scatter( x=consumption_data.Date, y=consumption_data.Consumption, mode='lines',name='lines'))
#fig = px.line(data, x=~Date,y = ~Consumption,name = "Consumption", type = 'scatter', mode = 'lines') 
#fig = fig.add_trace(data,y = ~Generation , name = 'Generation', mode = 'lines') 
#st.plotly_chart(fig)
