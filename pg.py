import requests
from datetime import datetime
import csv

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

def format_data(json_data):
    pp = 0.0
    pd_lst = []
    frmtd_data = [["Time", "Price", "% Diff", "Action", "Trade"]]
    for i, val in enumerate(json_data):
        tp = time_price(val)
        tim = tp['time']
        cp = tp['price']
        if i == 0:
            pd = 0
            pp = cp
        else:
            pd =  percentage_diff(cp, pp)
            pp = cp
            

        pd_lst.append([tim, cp, pd])

    for i, val in enumerate(pd_lst):
        if (i == len(pd_lst) - 1) or (i == 0):
            a=val
            a.append('H')
            frmtd_data.append(a)
        else:
            c_pd = float(val[2])
            f_pd = float(pd_lst[i+1][2])
            act = action(c_pd, f_pd)  
            a = val
            a.append(act)             
            frmtd_data.append(a)
    return frmtd_data

def save_csv(file_name, data_list):
    print(data_list[0])
    print(data_list[1])
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerows(data_list)

start_date = '2020-06-27'
end_date = '2020-06-28'
url = 'https://production.api.coindesk.com/v2/price/values/BTC?start_date={}T20:00&end_date={}T19:59&ohlc=false'.format(start_date, end_date)

resp = requests.get(url=url)
d = resp.json()

msg = d['message']
if msg == 'OK':
    data = d['data']['entries']
    ll = format_data(data)
    file_name = start_date + '--' + end_date + '.csv'
    save_csv(file_name, ll)
else:
    print('Err: Couldn\'t get json data')


data_list = [["SN", "Name", "Contribution"],
             [6, "Linus Torvalds", "Linux Kernel"],
             [2, "Tim Berners-Lee", "World Wide Web"],
             [3, "Guido van Rossum", "Python Programming"]]
