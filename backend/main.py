from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sklearn.metrics import mean_squared_error
import uvicorn
import pandas as pd
import joblib
import json
import random
from config import path_to_data, filename
from config import features_for_train
from train import Train
import os
import re
import math

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

def send_data_to_test():
    test_data = pd.read_csv('./data/dataset_test.csv')
    encoder = Train() 
    row = 3
    data_for_tr = test_data.copy() 
    test_show = [test_data.columns.values.tolist()] + test_data.values.tolist()
    test_x, test_y = encoder.normalize(data_for_tr, features_for_train.copy())
    return {
        "test_show": test_show,
        "test_x": test_x.to_dict(),
        "test_y": [test_y.values.tolist()],
        "test_y_pred": test_y
    }
### UPLOAD #######    
@app.post("/upload")
async def create_upload_file(file: UploadFile = File(...)):
    x = re.findall(r'([0-9]+ [0-9]+)', file.filename)
    filename = x[0].replace(' ', '_')

    docs = [f for f in os.listdir('./data/docx')]
    print(docs)
    for i in docs:
        os.remove(f'./data/docx/{i}')
    print(docs)
    docs = [f for f in os.listdir('./data/doc')]
    for i in docs:
        os.remove(f'./data/doc/{i}')

    docs = [f for f in os.listdir('./parse/json')]
    print(docs)
    for i in docs:
        os.remove(f'./parse/json/{i}')

    with open(f'./data/doc/{filename}.doc', 'wb') as f:
        f.write(file.file.read())
    
    os.system(f'python parse/doc_to_docx.py ./data/doc/{filename}.doc')
    os.system(f'python parse/save_to_csv.py {filename}')
    os.system(f'python parse/merge.py')


    return {"filename": file.filename}
### UPLOAD #######


### TABLE #######
@app.get("/tables")
def tables():
    data_list = [data.columns.values.tolist()] + data.values.tolist()
    return {'data': data_list[:400]}
### TABLE #######

### CROP_TEST #######
@app.get("/crop_test")
def crop_test():
    return send_data_to_test()

### CROP_TEST #######

### DASHBOARD #######
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
### DASHBOARD #######

### PREDICT #######
@app.post("/predict")
def predict(data_test: list):
    loaded_model = joblib.load(filename)
    data_test_x = pd.DataFrame(data_test[0])
    predicted = loaded_model.predict(data_test_x)
    predicted = str(predicted).replace('[','')
    predicted = str(predicted).replace(']','')
    predicted = predicted.split(' ')
    while("" in predicted): 
        predicted.remove("")

    for i, value in enumerate(predicted):
        if "\n" in value:
            predicted[i].replace('\n', '')
        predicted[i] = float(value)

    print(predicted)
    # print(data_test[1])
    # print(mean_squared_error(data_test[1], predicted))
    return {
        'predicted': predicted,
        # 'rmse': math.sqrt(mean_squared_error(pd.DataFrame(data_test[1]), predicted))
    }
    
### PREDICT #######
if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)