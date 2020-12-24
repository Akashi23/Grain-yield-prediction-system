import pandas as pd

df1 = pd.read_csv('./data/crop.csv')
df2 = pd.read_csv('./data/weather1.csv')
soil = {
    'Ақмола':'Темно-каштановые, Черноземы',
    'Ақтөбе':'Темно-каштановые, Черноземы, Каштановые',
    'Алматы':'Горные, Сероземы, Пески',
    'Атырау':'Светло-каштановые, Пески',
    'Батыс Қазақстан':'Темно-каштановые, Каштановые, Светло-каштановые',
    'Жамбыл':'Сероземы, Пески',
    'Қарағанды':'Каштановые, Светло-каштановые',
    'Қостанай':'Темно-каштановые, Черноземы',
    'Қызылорда':'Сероземы, Пески',
    'Маңғыстау':'Серо-бурые, бурые пустынные',
    'Оңтүстік Қазақстан':'Горные, Сероземы, Пески',
    'Павлодар':'Темно-каштановые',
    'Солтүстік Қазақстан':'Черноземы',
    'Шығыс Қазақстан':'Темно-каштановые, Каштановые, Горные',
    'Астана қаласы':'Темно-каштановые, Каштановые',
    'Алматы қаласы':'Горные, Сероземы, Пески',
}
col1 = []
col2 = []
for i in soil:
    col1.append(i)
    col2.append(soil[i])

d = {
    'region': col1,
    'soil':col2
}

d = pd.DataFrame(data=d)

df = pd.merge(df1, df2, on=['region','month', 'year'], sort=False)
df = pd.merge(df, d, on=['region'], sort=False)
df = df.sort_values(by=['year', 'month'])

df.to_csv('./data/dataset_test.csv', index=False)