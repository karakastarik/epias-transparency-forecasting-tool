import pandas as pd
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from lightgbm import LGBMRegressor
import plotly.graph_objects as go

def select_period(period):
    periods={"1 day":24,"2 days":48,"3 days":72,"1 week":168,"2 weeks":336,"3 weeks":504,"1 month":672}
    return periods[period]

#def select_algorithm(method):
#    algorithms = {
#    'LightGBM' : LGBMRegressor(),
#    'XGBoost': XGBRegressor(),
#    }
#    return algorithms[method]

def extract_features(df):
    df['hour'] = df['Date'].dt.hour
    df['month'] = df['Date'].dt.month
    df['quarter'] = df['Date'].dt.quarter
    df['dayofweek'] = df['Date'].dt.dayofweek
    df['dayofyear'] = df['Date'].dt.dayofyear
    df['dayofmonth'] = df['Date'].dt.day
    df['weekofyear'] = df['Date'].dt.week
    df=pd.get_dummies(df, columns = ["hour"], prefix = ["hour"])
    #df=pd.get_dummies(df, columns = ["month"], prefix = ["month"])
    df=pd.get_dummies(df, columns = ["quarter"], prefix = ["quarter"])
    df=pd.get_dummies(df, columns = ["dayofweek"], prefix = ["dayofweek"])

    return df
 
def forecast(data,periods,selected_algorithm):
    #forecast_start_date=datetime.date.today()-datetime.timedelta(days=6095)
    #forecast_end_date=datetime.date.today()
    #forecast_consumption = consumption_realtime(startDate=str(forecast_start_date),endDate=str(forecast_end_date))
    date=pd.date_range(start=pd.to_datetime(data.Date).tail(1).iloc[0], periods=periods, freq='H')
    date=pd.DataFrame(date).rename(columns={0:"Date"})
    forecast_consumption=pd.merge(data ,date,how='outer')
    forecast_consumption=extract_features(forecast_consumption)
    forecast_consumption["rolling_mean"] = forecast_consumption["Consumption"].rolling(window=periods, min_periods=1).mean().shift(1).values
    forecast_consumption["rolling_max"] = forecast_consumption["Consumption"].rolling(window=periods, min_periods=1).max().shift(1).values
    forecast_consumption["rolling_min"] = forecast_consumption["Consumption"].rolling(window=periods, min_periods=1).min().shift(1).values
    forecast_consumption=forecast_consumption[1:]
    split_date = pd.to_datetime(forecast_consumption.Date).tail(periods).iloc[0]

    forecast_consumption_historical = forecast_consumption.loc[forecast_consumption.Date <= split_date].copy()
    forecast_consumption_predict = forecast_consumption.loc[forecast_consumption.Date > split_date].copy()
    forecast_consumption_historical.set_index("Date",inplace=True)
    forecast_consumption_predict.set_index("Date",inplace=True)

    y=forecast_consumption_historical["Consumption"]
    X=forecast_consumption_historical.drop("Consumption",axis=1)
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.05,shuffle = False)
    X_pred=forecast_consumption_predict.drop("Consumption",axis=1)

    if selected_algorithm=="LightGBM":
        lgb_model=LGBMRegressor(learning_rate= 0.1, max_depth= 7, n_estimators=2000)
        lgb_model.fit(X_train, y_train, eval_set=[(X_train, y_train), (X_val, y_val)],early_stopping_rounds=100,eval_metric="rmse",verbose=True)
        y_pred=lgb_model.predict(X_pred)
        y_train_pred=lgb_model.predict(X_train)
        y_val_pred=lgb_model.predict(X_val)
    else:
        xgb_model = XGBRegressor(colsample_bytree = 1, learning_rate = 0.5, max_depth = 5, n_estimators = 200)
        xgb_model.fit(X_train, y_train, eval_set=[(X_train, y_train), (X_val, y_val)],early_stopping_rounds=100,eval_metric="rmse",verbose=True)
        y_pred=xgb_model.predict(X_pred)
        y_train_pred=xgb_model.predict(X_train)
        y_val_pred=xgb_model.predict(X_val)

    print("Final Train RMSE",mean_squared_error(y_train, y_train_pred, squared=False))
    print("Final Validation RMSE:",mean_squared_error(y_val, y_val_pred, squared=False))

    y=y.loc['2021-04-01':]

    return y,y_pred,X_pred


def plot_forecast(data,periods,selected_algorithm):
    y, y_pred, X_pred= forecast(data,periods,selected_algorithm)
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=y.index,y=y,name='Historical Data'))
    fig1.add_trace(go.Scatter(x=X_pred.index,y=y_pred,name='Forecast'))
    fig1.update_layout(title='Consumption Forecast')
    fig1.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
    return fig1

