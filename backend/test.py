import pandas as pd

dataset = pd.read_csv('./data/dataset.csv')
dataset_test = pd.read_csv('./data/dataset_test.csv')

df = pd.concat([dataset, dataset_test], axis=0)
df.to_csv('./data/dataset.csv', index=False)