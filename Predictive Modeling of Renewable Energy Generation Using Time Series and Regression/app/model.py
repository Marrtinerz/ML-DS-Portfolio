import numpy as np
import pandas as pd
import xgboost as xgb
import pickle

#defining the base directory here
base = 'C:/Users/user/OneDrive/Documents/DATA SCIENCE/Data Science Projects/ML-DS-Portfolio/Predictive Modeling of Renewable Energy Generation Using Time Series and Regression/app'
reg = xgb.XGBRegressor()
#loading the pickle file
model = pickle.load(open(f'{base}/model2.pkl', "rb"))
#model = reg.load_model(f'{base}/model2.json')

def create_f(df):
    df = df.copy()
    df['hour'] = df.index.hour
    df['minute'] = df.index.minute
    df['day'] = df.index.day
    df['month'] = df.index.month
    df['year'] = df.index.year
    df['dayofweek'] = df.index.dayofweek
    df['dayofyear'] = df.index.dayofyear
    df['weekofyear'] = df.index.isocalendar().week
    
    return df


def create_pd(fr,to):
    new = pd.date_range(fr+' 12:00:00+00:00',to+' 12:00:00+00:00', freq='10min')
    new = pd.DataFrame(index=new)
    new = create_f(new)
    return new
