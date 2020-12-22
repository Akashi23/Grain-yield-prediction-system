from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
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

data = pd.read_csv(path_to_data)

def histogram(feature, func):
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


def line(feature: str, func: str, region: str) -> list:
    list_year = [str(x) for x in range(2012, 2021)]
    all_sum_list = []
    all_sum_list.append(['year', region])

    
    for j in list_year:
        summa = []
        summa.append(j)
        if func == "sum":
            data_all = data.query(f'region == "{region}" and year == {j}')[feature].sum()
        elif func == "avg":
            data_all = data.query(f'region == "{region}" and year == {j}')[feature].mean()
        else:
            data_all = data.query(f'region == "{region}" and year == {j}')[feature].mean()
        summa.append(float(f"{data_all:.1f}"))

        all_sum_list.append(summa)

    return all_sum_list


def mini_line_res(feature, func):
    region = list(data['region'].unique())
    data_for_return = {}

    for i in region:
        data_for_return[i] = line(feature, func, i)

    return data_for_return


def show_soil():
    region = list(data['region'].unique())
    data_for_return = []
    data_for_return.append(['Регион', 'Почва'])

    for i in region:
        data_soil = data.query(f'region == "{i}"')['soil'].unique()[0]
        mid = []
        mid.append(i)
        mid.append(data_soil)
        data_for_return.append(mid)
    
    return data_for_return


@app.get("/tables")
def tables():
    data_list = [data.columns.values.tolist()] + data.values.tolist()
    return {'data': data_list[:400]}

@app.get("/dashboard")
def dashboard_humidity():
    region = list(data['region'].unique())
    crops = []
    
    data_list = {
        "humidity": histogram('humidity', 'avg'),
        "precip": histogram('precipMM', 'sum'),
        "snow": histogram('totalSnow_cm', 'sum'),
        "crop": histogram('crop', 'sum'),
        "crops": mini_line_res('crop', 'sum'),
        "soils": show_soil()
    }
    return data_list

@app.post("/predict")
def predict(data_x_test):
    loaded_model = joblib.load(filename)
    predicted = loaded_model.predict(data_x_test)
    return {'predicted': predicted}

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)