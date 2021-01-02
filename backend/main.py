import os
import re
import math
import json
import random
import uvicorn
import pandas as pd
import joblib

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
# from sklearn.metrics import mean_squared_error
from config import path_to_data, filename
from config import features_for_train
from train import Train
from data_sender_to_db import send_dataset_test

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


def mean_30(array):
    summa = 0
    for i in array:
        summa += i
    # return max(array)
    return float(summa/len(array))


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
@app.post("/predict")
def predict(data_test: list):
    loaded_model = joblib.load(filename)
    data_test_x = pd.DataFrame(data_test[0])
    predicted = loaded_model.predict(data_test_x)
    predicted = str(predicted).replace('[', '')
    predicted = str(predicted).replace(']', '')
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
    predicted.append(len(predicted))
    return {
        'predicted': predicted,
        # 'rmse': math.sqrt(mean_squared_error(pd.DataFrame(data_test[1]), predicted))
    }


### PREDICT #######
if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
