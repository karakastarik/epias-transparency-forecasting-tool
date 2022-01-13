from contextlib import suppress
from functions import mcp, consumption_realtime # import functions.py
from forecasting import  select_period, plot_forecast
import streamlit as st #streamlit
import datetime 
import pandas as pd
import plotly.graph_objects as go
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(page_title ="Forecasting Tool")

tabs = ["Forecasting","Data Visualization","About"]

page = st.sidebar.radio("Tabs",tabs)

if page == "Forecasting":

    st.markdown("<h1 style='text-align: center;'>Forecasting</h1>", unsafe_allow_html=True)
    st.markdown("""We use two algorithms (for now) for forecasting. The documentation of the algorithms are:
      **[XGBoost](https://xgboost.readthedocs.io/en/latest/python/index.html)**, 
      **[LightGBM](https://lightgbm.readthedocs.io/en/latest/)**""")
    selected_period=st.selectbox("Select a forecasting period",["1 day","2 days","3 days","1 week","2 weeks","3 weeks"])
    selected_algorithm=st.selectbox("Select an algorithm",["XGBoost","LightGBM"])
    button=st.button("Forecast")
    if button==True:
        with st.spinner("Forecasting in progress. Please wait..."):
            forecast_start_date=datetime.date.today()-datetime.timedelta(days=6095)
            forecast_end_date=datetime.date.today()
            print("Importing data for prediction") #log
            try:
                consumption_data = consumption_realtime(startDate=str(forecast_start_date),endDate=str(forecast_end_date))
                fig1=plot_forecast(consumption_data,select_period(selected_period),selected_algorithm)
                st.plotly_chart(fig1)
            except:
                st.warning("There is a problem about database. Please try again later...")

if page=="Data Visualization":
    #Start and End Dates
    start_date=st.sidebar.date_input(label="Start Date", value=datetime.date.today()-datetime.timedelta(days=10))
    end_date=st.sidebar.date_input(label="End Date", value=datetime.date.today())
    
    st.markdown("<h1 style='text-align: center;'>Data Visualization</h1>", unsafe_allow_html=True)
    st.markdown("""This tool aims to generate time series forecast for Turkey's electric power industry. Data comes from
     **[EPIAS Transparency Platform](https://seffaflik.epias.com.tr/transparency/index.xhtml)** and updated hourly.""")
    if end_date > start_date or end_date == start_date:
        
        consumption_data_vis = consumption_realtime(startDate=str(start_date),endDate=str(end_date))
        cons_describe=pd.DataFrame(consumption_data_vis.describe()).reset_index().rename(index=str,columns={"index":"Statistic"})
        
        #Consumption-Descriptive Statistics
        st.markdown("<h3 style='text-align: center; color: black;'>Consumption-Descriptive Statistics</h3>", unsafe_allow_html=True)
        st.table(cons_describe)
        
        #Consumption-Hourly Graph
        fig_cons = go.Figure()
        fig_cons.add_trace(go.Scatter(x=consumption_data_vis.Date, y=consumption_data_vis.Consumption, mode='lines',name='Consumption (MWh)'))
        fig_cons.update_layout(xaxis_title='Date',yaxis_title='Consumption (MWh)',plot_bgcolor='rgba(0,0,0,0)')
        st.markdown("<h3 style='text-align: center; color: black;'>Hourly Consumption (MWh)</h3>", unsafe_allow_html=True)
        st.plotly_chart(fig_cons)

        #Import MCP data from the source.
        mcp_data = mcp(startDate=str(start_date),endDate=str(end_date))
        mcp_describe=pd.DataFrame(mcp_data.describe()).reset_index().rename(index=str,columns={"index":"Statistic"})
        
        #MCP-Descriptive Statistics
        st.markdown("<h3 style='text-align: center; color: black;'>Market Clearing Price-Descriptive Statistics</h3>", unsafe_allow_html=True)
        st.table(mcp_describe)
        
        #MCP-Hourly Graph
        st.markdown("<h3 style='text-align: center; color: black;'>Market Clearing Price-TL</h3>", unsafe_allow_html=True)
        fig_mcp = go.Figure()
        fig_mcp.add_trace(go.Scatter(x=mcp_data.Date, y=mcp_data.MCP_TL, mode='lines',name='MCP TL'))
        fig_mcp.update_layout(xaxis_title='Date',yaxis_title='MCP',plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_mcp)

    else:
        st.warning("Start date cannot be greater than end date. Please re-enter dates.")

if page == "About":
    st.header("About")
    st.write("v1.0")
    st.write("Author:")
    st.markdown(""" **[Tarik Karakas](https://tr.linkedin.com/in/karakastarik)**""")
    st.markdown("""**[Source code](https://github.com/karakastarik/epias-transparency-forecasting-tool)**""")

#Real time generation
#real_time_gen_data = real_time_gen(startDate=str(start_date),endDate=str(end_date))
#real_time_gen_data.head()

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

#cons_markdown = f"Average hourly consumption in the last **{consumption_data.Date.count()}** hours is: **{consumption_data.Consumption.mean():.2f}**."
#st.markdown(cons_markdown)

#fig = px.line(data, x=~Date,y = ~Consumption,name = "Consumption", type = 'scatter', mode = 'lines') 
#fig = fig.add_trace(data,y = ~Generation , name = 'Generation', mode = 'lines') 

