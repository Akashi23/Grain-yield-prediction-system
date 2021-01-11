import os
import re
import math
import csv
import json
import random
import uvicorn
import pandas as pd
import joblib

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sklearn.metrics import mean_squared_error
from config import path_to_data, filename, filename_scaler
from config import features_for_train
from train import Train
from data_sender_to_db import send_dataset_test, send_dataset, send_dataset_train_test, send_dataset_new_test

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


def send_data_to_test():
    test_data = pd.read_csv('./data/dataset_test.csv')
    encoder = Train()
    data_for_tr = test_data.copy()
    test_show = [test_data.columns.values.tolist()] + test_data.values.tolist()
    test_x, test_y = encoder.normalize(data_for_tr, features_for_train.copy())
    print(len(test_y.unique().tolist()))
    return {
        "test_show": test_show,
        "test_x": test_x.to_dict(),
        "test_y": [test_y.unique().tolist()],
        "test_y_pred": test_y
    }


### UPLOAD #######
@app.post("/upload")
async def create_upload_file(file: UploadFile = File(...)):

    docs = [f for f in os.listdir('./data/docx')]
    for i in docs:
        os.remove(f'./data/docx/{i}')

    docs = [f for f in os.listdir('./data/doc')]
    for i in docs:
        os.remove(f'./data/doc/{i}')

    docs = [f for f in os.listdir('./parse/json')]
    for i in docs:
        os.remove(f'./parse/json/{i}')

    x = re.findall(r'([0-9]+ [0-9]+)', file.filename)
    filename = x[0].replace(' ', '_')

    with open(f'./data/doc/{filename}.doc', 'wb') as f:
        f.write(file.file.read())

    os.system(f'python parse/doc_to_docx.py ./data/doc/{filename}.doc')
    os.system(f'python parse/save_to_csv.py {filename}')
    os.system(f'python parse/merge.py')
    send_dataset_test(False)
    return {"filename": file.filename}


### UPLOAD #######


@app.get("/crop_test")
def crop_test():
    return send_data_to_test()

### PREDICT #######


@app.get("/predict")
def predict():
    test_data = pd.read_csv('./data/dataset_test.csv')
    
    data_all = data.copy()
    
    loaded_model = joblib.load(filename)
    
    encoder = joblib.load(filename_scaler)
    
    train = Train()
    
    object_types = ['soil', 'region', 'weatherDesc', 'winddir16Point']
    
    data_for_tr = test_data.copy()
    data_y_test = test_data['crop']
    
    for i in object_types:
        le = train.encoder(data_all, i)
        data_for_tr[i] = le.transform(data_for_tr[i])

    data_for_tr = data_for_tr[features_for_train.copy()].drop(columns=['crop'])
    print(data_for_tr)

    features = features_for_train.copy()
    features.remove('crop')

    data_x_test = pd.DataFrame(
        encoder.transform(data_for_tr),
        columns=features)

    data_y_pred = loaded_model.predict(data_x_test)

    print(math.sqrt(mean_squared_error(data_y_test, data_y_pred)))
    print(data_y_test, pd.DataFrame(data_y_pred))

    data_y_test_db = pd.DataFrame(
        data_y_test,
        columns=['crop']).reset_index(
        drop=True)

    data_y_pred_db = pd.DataFrame(data_y_pred, columns=['crop_pred'])
    date = data['date']
    
    data_x_test = data_x_test.merge(date, left_index=True, right_index=True)

    print(data_x_test['date'])

    data_x_test_db = data_x_test.reset_index(drop=True)
    
    result = pd.concat(
        [data_x_test_db, data_y_test_db, data_y_pred_db], axis=1)
    result.to_csv('data/dataset_new_test.csv', index=False)
    
    send_dataset_new_test(False)
    
    os.system('python train.py')

    dataset = pd.read_csv('./data/dataset.csv')
    dataset_test = pd.read_csv('./data/dataset_test.csv')

    df = pd.concat([dataset, dataset_test], axis=0)
    df.to_csv('./data/dataset.csv', index=False)

    send_dataset(False)

    return {
        'predicted': str(data_y_pred),
    }


### PREDICT #######
if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
