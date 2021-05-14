
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
    
    query = "market/day-ahead-mcp?startDate="+f'{startDate}'+"&endDate="+f'{endDate}'
    json_result = get_request_result(query)
    df = pd.DataFrame(json_result["body"]["dayAheadMCPList"])
    df["Hour"] = df["date"].apply(lambda h: int(h[11:13]))
    df["Date"] = pd.to_datetime(df["date"].apply(lambda d: d[:10]))
    df.rename(index=str, columns={"price": "MCP_TL","priceUsd": "MCP_USD","priceEur": "MCP_EUR"}, inplace=True)
    df = df[["Date", "Hour", "MCP_TL","MCP_USD","MCP_EUR"]]
    return df


def consumption_realtime(startDate, endDate):

    query = "consumption/real-time-consumption?"+"startDate="+f'{startDate}'+"&endDate="+f'{endDate}'

    json_result = get_request_result(query)

    df = pd.DataFrame(json_result["body"]["hourlyConsumptions"])
    df["Hour"] = df["date"].apply(lambda h: int(h[11:13]))
    df["Date"] = pd.to_datetime(df["date"].apply(lambda d: d[:10]))
    df.rename(index=str, columns={"consumption": "Consumption"}, inplace=True)
    df = df[["Date", "Hour", "Consumption"]]

    return df
#not completed  
def real_time_gen(startDate, endDate):
    '''
    Parameters:
    startDate: Start date in YYYY-MM-DD format.
    endDate: End date in YYYY-MM-DD format.

    '''
    query = "production/real-time-generation?startDate="+f'{startDate}'+"&endDate="+f'{endDate}'
    json_result = get_request_result(query)

    df = pd.DataFrame(json_result["body"]["hourlyGenerations"])
    df["Hour"] = df["date"].apply(lambda h: int(h[11:13]))
    df["Date"] = pd.to_datetime(df["date"].apply(lambda d: d[:10]))
    return df

