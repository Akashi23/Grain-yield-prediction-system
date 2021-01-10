import pandas as pd
from parse_docx_func import parse_docx
from os import listdir
from os.path import isfile, join
from parse_json import parse
from request_api import request_to_api
import sys

def region_parse():
    docs = [f for f in listdir('./data/docx')]
    print(docs)
    data = []
    columns = ['year', 'month', 'region', 'crop']
    for doc in docs:
        info = parse_docx(doc)
        doc = doc.replace('.docx', '')
        month = doc[0:2].replace('_', '')

        year = doc.replace(f'{month}_', '')
        # if int(month) == 1:
        #     year = str(int(doc.replace(f'{month}_', ''))-1)
        #     month = str(12)
        # else:
        #     year = str(doc.replace(f'{month}_', ''))
        #     month = str(int(month) - 1) 
        i = 0
        for region in info:
            i += 1
            if i <= 10:
                continue 
            else:
                region_r = region
                if region == 'Сұлтан қаласы':
                    region_r = 'Астана қаласы'
                if region == 'Шымкент қаласы':
                    region_r = 'Оңтүстік Қазақстан'
                print(region)
                data.append([year, month, region_r, float(info[region])])

    df = pd.DataFrame(data=data, columns=columns)
    df.to_csv('./data/crop.csv', index=False)
    print(df)


def weather_parse(year, month):

    cities_dict = [
        {'aktobe': 'Ақтөбе'},
        {'almaty': 'Алматы қаласы'},
        {'akmola': 'Ақмола'},
        {'atyrau': 'Атырау'},
        {'oral': 'Батыс Қазақстан'},
        {'zhambyl': 'Жамбыл'},
        {'karaganda':'Қарағанды'},
        {'kostanay':'Қостанай'},
        {'kyzylorda': 'Қызылорда'},
        {'mangystau':'Маңғыстау'},
        {'ontustik': 'Оңтүстік Қазақстан'},
        {'pavlodar': 'Павлодар'},
        {'soltustik':'Солтүстік Қазақстан'},
        {'shygys':'Шығыс Қазақстан'},
        {'astana': 'Астана қаласы'},
        ]
    
    cities_str = {
        'aktobe': 'aktobe+kazakhstan',
        'almaty': 'almaty+kazakhstan',
        'akmola': 'akmola+kazakhstan',
        'atyrau': 'atyrau+kazakhstan',
        'oral': 'oral+kazakhstan',
        'zhambyl': 'zhambyl+kazakhstan',
        'karaganda':'karaganda+kazakhstan',
        'kostanay':'kostanay+kazakhstan',
        'kyzylorda': 'kyzylorda+kazakhstan',
        'mangystau':'aktau+kazakhstan',
        'ontustik': 'shymkent+kazakhstan',
        'pavlodar': 'pavlodar+kazakhstan',
        'soltustik':'akmola+kazakhstan',
        'shygys':'semey+kazakhstan',
        'astana': 'astana+kazakhstan',
        }

    for i in cities_str:
        city = i
        print(city)
        request_to_api(year, int(month), cities_str[city], city)

    docs = [f for f in listdir('parse/json')]
    print(docs)
    data = pd.DataFrame()
    almaty = {}
    for doc in docs:
        info = parse(doc)
        for city in cities_dict:
            for i in city:
                if str(i) in doc:
                    info['region'] = city[i]
                    if 'almaty' in doc and i == 'almaty2':
                        almaty = info.copy()
                        almaty['region'] = city['almaty2']
                        data = pd.concat([data, almaty], ignore_index=True)
        print(doc)
        data = pd.concat([data, info], ignore_index=True)


    data.to_csv('./data/weather1.csv', index=False)
    print(data)


if __name__ == "__main__":
    year = sys.argv[1].replace('_', ' ').split(' ')[1]
    month = sys.argv[1].replace('_', ' ').split(' ')[0]
    weather_parse(year, month)
    region_parse()