from datetime import datetime
from binance.client import Client
import requests
import json
import time
import pickle
import platform


min_mc = 1000000000

def get_lc_key():
    pt = platform.system()
    fn = 'C:/Users/HENOK/Documents/Bkey/lc-key.pickle' if pt == 'Windows' else '/home/ubuntu/Bkey/lc-key.pickle'
    val = read_pickle_file(fn)
    return read_pickle_file(fn)['lc_key']


def get_trending_coins():
    lc_key = get_lc_key()
    lc_url = f'https://api2.lunarcrush.com/v2/assets?data=market&type=fast&key={lc_key}'
    x = requests.get(lc_url)
    d={}
    data=json.loads(x.text)['data']
    for i in data:
        mc=i['mc']
        if mc>min_mc:
            d[i['s']]=i['gs']
    srtd = sorted(d.items(), key=lambda x: x[1])
    s = [srtd[i] for i in range(-1,-11,-1)]
    srtd_lst = [i[0] for i in s]
    return srtd_lst


def read_pickle_file(fn):
    with open(fn, 'rb') as handle:
        val = pickle.load(handle)
    return val

def write_pickle(fn, val):
    try:
        with open(fn, 'wb') as handle:
            pickle.dump(val, handle, protocol=pickle.HIGHEST_PROTOCOL)
            print(f'\n{fn} exported')
    except:
        print(f'\nCould not export {fn}')


def get_client():
    pt = platform.system()
    fn = 'C:/Users/HENOK/Documents/Bkey/bkey.pickle' if pt == 'Windows' else '/home/ubuntu/Bkey/bkey.pickle'
    val = read_pickle_file(fn)
    api_key=val['binance_api_key']
    api_secret=val['binance_api_secret']
    return Client(api_key, api_secret)

def get_historical_data(client, pair_to_export, from_date, to_date):
    # valid intervals - 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
    # @return OHLCV
    return client.get_historical_klines(pair_to_export, Client.KLINE_INTERVAL_1MINUTE, from_date, to_date)


def get_usdt_balance(client, coin):
    info = client.get_account()['balances']
    for i in info:
        asset = i["asset"]
        if asset == coin:
            free = float(i['free'])
            locked = float(i['locked'])
            return {'free': free, 'locked': locked}


def get_current_price(client, pair):
    ts = int(time.time())*1000
    to_date = int(time.time())
    from_date = to_date - 1
    price = get_historical_data(client, pair, from_date, to_date)
    print(price)

def get_usdt_pair_coins(client):
	r=[]
	exchange_info = client.get_exchange_info()
	for s in exchange_info['symbols']:
		pair = s['symbol']
		if pair[-4:] == 'USDT':
			r.append(pair[:-4])
	return r

def get_quantity(client, pair):
    price = get_current_price(client, pair)

def buy(client, pair, quantity):
    order = client.creat_order(
        symbol=pair,
        side='SIDE_BUY',
        type='ORDER_TYPE_MARKET',
        quantity=quantity
    )

client = get_client()
min_usdt = 50.0
filtered_coins = ['USDT', 'BUSD']
trending_coins = get_trending_coins()
all_coins = get_usdt_pair_coins(client)

print('trending_coins: ', trending_coins)
# for coin in trending_coins:
#     usdt_balance = get_usdt_balance(client, 'USDT')['free']
#     if (usdt_balance > min_usdt):
#         if(coin in all_coins):
#             print('Can Place Order: $', usdt_balance)
#             print('Can buy ', coin)
#             pair = coin+'USDT'
#             get_current_price(client, pair)
#         else:
#             print(coin, ' not in binance')
#     else:
#         print('insufficient USDT: $', usdt_balance)
#         break
get_quantity(client, 'ADAUSDT')