import json
import pandas as pd

def parse(filename):
    with open(f"parse/json/{filename}", "r") as f:
        data = f.read()

    weather = json.loads(data)

    df = pd.DataFrame(weather['data']['weather'])
    df2 = pd.DataFrame()
    df['date'] = pd.to_datetime(df['date'])
    print(df['date'])
    s = 0

    df['year'] = df['date'].dt.year
    df['month']= df['date'].dt.month
    df['day']= df['date'].dt.day
    
    for num, i in enumerate(weather['data']['weather']):
        date = df['date'][num]
        for j in i['hourly']:
            j['date'] = date
            df2 = pd.concat([df2, pd.DataFrame(j)], ignore_index=True)
            df2['weatherDesc'] = j['weatherDesc'][0]['value']

    df2['date'] = pd.to_datetime(df2['date'])
    df = df.drop(columns=['astronomy', 'hourly'])
    print(df2)
    s = pd.merge_asof(df, df2, on="date")
    
    s = s.drop(s.tail(1).index, axis=0)
    s = s.drop('weatherIconUrl', axis=1)
    return s

if __name__ == "__main__":
    s = parse('aktobe_2012_1.json')
    s.to_csv('file.csv', index=False)