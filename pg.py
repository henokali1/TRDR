import requests
from datetime import datetime

def time_price(val):
    ts = int(str(val[0])[:-3])
    td = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    tim = td.split(' ')[1]
    price = val[1]
    return {'time': tim, 'price': price}

def percentage_diff(cp, pp):
    return (100.0*(cp-pp))/pp

def action(c_pd, f_pd):
    if((c_pd < 0) and (f_pd < 0)):
        return 'H'
    if((c_pd < 0) and (f_pd > 0)):
        return 'B'
    if((c_pd > 0) and (f_pd < 0)):
        return 'S'
    if((c_pd > 0) and (f_pd > 0)):
        return 'H'
    
start_date = '2020-06-27'
end_date = '2020-06-28'
url = 'https://production.api.coindesk.com/v2/price/values/BTC?start_date={}T20:00&end_date={}T19:59&ohlc=false'.format(start_date, end_date)

resp = requests.get(url=url)
d = resp.json()

msg = d['message']
data = d['data']['entries']

