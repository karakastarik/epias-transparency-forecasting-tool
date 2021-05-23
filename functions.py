
import requests
import json
import pandas as pd

def get_request_result(query):
    #main_url = "https://seffaflik.epias.com.tr/transparency/service/market/"

    url = "https://seffaflik.epias.com.tr/transparency/service/"+query

    payload = {}
    headers = {
    'Cookie': 'TS01f69930=01cbc7c0b229af3f9e170f80092f828abac28c9cacff2f44fbd6391713e0e3f0af97eecc2694f5fc77aefc033595cc62fe9c469b52'
        }
    #headers = {'x-ibm-client-id': "",'accept': "application/json"} #yedek headers

    response = requests.get(url, headers=headers, data = payload,verify=False)

    json_data = json.loads(response.text.encode('utf8'))

    return json_data
            
def mcp(startDate, endDate):
    '''
    Market Clearing Price TL-USD-EUR
    Parameters:
    startDate: Start date in YYYY-MM-DD format.
    endDate: End date in YYYY-MM-DD format.
    '''
    
    query = "market/day-ahead-mcp?startDate="+f'{startDate}'+"&endDate="+f'{endDate}'
    json_result = get_request_result(query)
    df = pd.DataFrame(json_result["body"]["dayAheadMCPList"])
    df.date=pd.to_datetime(df.date.str[:16])
    df.rename(index=str, columns={"date":"Date","price": "MCP_TL","priceUsd": "MCP_USD","priceEur": "MCP_EUR"}, inplace=True)
    df = df[["Date", "MCP_TL","MCP_USD","MCP_EUR"]]
    
    return df

def consumption_realtime(startDate, endDate):
    '''
    Real time consumption
    Parameters:
    startDate: Start date in YYYY-MM-DD format.
    endDate: End date in YYYY-MM-DD format.
    '''

    query = "consumption/real-time-consumption?"+"startDate="+f'{startDate}'+"&endDate="+f'{endDate}'
    json_result = get_request_result(query)
    df = pd.DataFrame(json_result["body"]["hourlyConsumptions"])
    df.date=pd.to_datetime(df.date.str[:16])
    df.rename(index=str, columns={"date": "Date","consumption": "Consumption"}, inplace=True)
    df = df[["Date", "Consumption"]]

    return df

def real_time_gen(startDate, endDate):
    '''
    Real time generation by sources.
    Parameters:
    startDate: Start date in YYYY-MM-DD format.
    endDate: End date in YYYY-MM-DD format.
    '''

    query = "production/real-time-generation?startDate="+f'{startDate}'+"&endDate="+f'{endDate}'
    json_result = get_request_result(query)
    df = pd.DataFrame(json_result["body"]["hourlyGenerations"])
    df.date=pd.to_datetime(df.date.str[:16])
    df.rename(index=str, 
        columns={"date":"Date","fueloil": "Fuel Oil","gasOil":"Gas Oil","blackCoal":"Black Coal",
        "lignite":"Lignite","geothermal":"Geothermal","naturalGas":"Natural Gas","river":"River","dammedHydro":"Dammed Hydro","lng":"LNG",
        "biomass":"Biomass","naphta":"Naphta","importCoal":"Import Coal","asphaltiteCoal":"Asphaltite Coal","wind":"Wind",
        "nucklear":"Nucklear","sun":"Sun","importExport":"Import-Export","total":"Total"}, inplace=True)
    
    df = df[["Date","Total","Natural Gas","Dammed Hydro","Fuel Oil","Gas Oil","Black Coal","Lignite","Geothermal","River",
    "LNG","Biomass","Naphta","Import Coal","Asphaltite Coal","Wind","Nucklear","Sun","Import-Export"]]
    
    return df
