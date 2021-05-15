#this script is currently under development and will not affect the tool.
import numpy as np
import pandas as pd
from xgboost import XGBRegressor
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, ExtraTreesRegressor
from sklearn.svm import LinearSVR
from lightgbm import LGBMRegressor

def select_algorithm(method):
    algorithms = {
    'LightGBM' : LGBMRegressor(),
    'Decision Tree' :DecisionTreeRegressor(),
    'Linear Regression': LinearRegression(),
    'K-Nearest Neighbors': KNeighborsRegressor(),
    'Random Forest': RandomForestRegressor(),
    'Gradient Boosting': GradientBoostingRegressor(),
    'XGBoost': XGBRegressor(verbosity = 0),
    'Support Vector Machines': LinearSVR(),
    'Extra Trees': ExtraTreesRegressor(),
     }
    
    return algorithms[method]

