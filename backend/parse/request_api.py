import requests as req
import time

def request_to_api(year, month, city, city_str):
    api_key = 'a9c2e93b038b43848f5111151202810'

    date = f'{year}-{month}-01'
    enddate = f'{year}-{month+1}-01'
    if month == 9:
        date = f'{year}-0{month}-01'
        enddate = f'{year}-{month+1}-01'
    elif month < 9:
        date = f'{year}-0{month}-01'
        enddate = f'{year}-0{month+1}-01'
    elif month == 12:
        enddate = f'{year+1}-{1}-01'
        
    url = f'https://api.worldweatheronline.com/premium/v1/past-weather.ashx?q={city}&date={date}&enddate={enddate}&key={api_key}&tp=24&format=json'

    res = req.get(url)

    with open(f'parse/json/{city_str}_{year}_{month}.json', 'w') as f:
        f.write(res.text)
    print(res.text)
    time.sleep(1)