from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import pandas as pd
import joblib
import json

from config import path_to_data, filename

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def histogram(feature, func):
    data = pd.read_csv(path_to_data)
    list_year = [str(x) for x in range(2012, 2021)]
    summa = []
    list_year.insert(0, "region")
    summa.append(list_year)
    region = list(data['region'].unique())

    for i in region:
        all_sum_list = []
        for j in list_year:
            if func == "sum":
                data_all = data.query(f'region == "{i}" and year == {j}')[feature].sum()
            elif func == "avg":
                data_all = data.query(f'region == "{i}" and year == {j}')[feature].mean()
            else:
                data_all = data.query(f'region == "{i}" and year == {j}')[feature].mean()
            all_sum_list.append(float(f"{data_all:.1f}"))
        all_sum_list.pop(0)
        all_sum_list.insert(0, i)
        summa.append(all_sum_list)

    return summa

@app.get("/tables")
def tables():
    data = pd.read_csv(path_to_data)
    data_list = [data.columns.values.tolist()] + data.values.tolist()
    return {'data': data_list[:400]}

@app.get("/dashboard")
def dashboard_humidity():
    data = {
        "humidity": histogram('humidity', 'avg'),
        "precip": histogram('precipMM', 'sum'),
        "snow": histogram('totalSnow_cm', 'sum'),
        "crop": histogram('crop', 'sum')
    }
    return data

# @app.get("/dashboard_temp")
# def dashboard_temp():
#     data = pd.read_csv(path_to_data)
#     data_to_send = {
#         'temp': [data['maxtempC'].columns.values.tolist()] + data['maxtempC'].values.tolist(),
#         'date': [data['date'].columns.values.tolist()] + data['date'].values.tolist(),
#         'region': [data['region'].columns.values.tolist()] + data['region'].values.tolist(),
#         }

#     return data_to_send

@app.post("/predict")
def predict(data_x_test):
    loaded_model = joblib.load(filename)
    predicted = loaded_model.predict(data_x_test)
    return {'predicted': predicted}