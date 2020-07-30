import requests
import ast
import json
import time
from datetime import datetime
from statistics import mean


prev_price = 0.0
prev_vol = 0.0

def read_file(fn):
	with open(fn,'r') as f:
		rd = f.read()
	sp = rd.split('\n')
	del sp[0]
	del sp[-1]
	return sp

def pay_load_format(val):
	sp = val.split(',')
	payload = {
		"instances": [
			{
				"Price": float(sp[0]),
				"Volume": float(sp[1]),
				"Price_PD": float(sp[2]),
				"Volume_PD": float(sp[3]),
				"Price_PD_bn_Trades": float(sp[4]),
				"Volume_PD_bn_Trades": float(sp[5]),
				"Mins_bn_Trade": int(sp[6]),
				"H_Price_PD": float(sp[7]),
				"H_Price_PD_bn_Trades": float(sp[8]),
				"H_Volume_PD_bn_Trades": float(sp[9]),
				"H_Mins_bn_Trade": int(sp[10])
			}
		]
	}
	
	return(payload)


def pred(payload):
	# r = requests.post("http://34.83.91.155:8080/predict", json=payload).text
	r = requests.post("http://localhost:8080/predict", json=payload).text
	p = ast.literal_eval(r)
	row_pred = p['predictions'][0]
	scores = row_pred['scores']
	classes = row_pred['classes']
	confid_score = max(scores)
	pred_index = scores.index(confid_score)
	prediction = classes[pred_index]
	return prediction

def inp_pred():
	while 1:
		d = input("Data: ")
		if (d == 'q' or d == 'Q'):
			break
		else:
			d = d.replace('\n','')
			sp = d.split(',')
			actual_action = sp[-1]

			payload = pay_load_format(d)

			pred(payload, actual_action, 3)

def current_min_trades():
	base = 'https://api.binance.com'
	q = '/api/v3/trades'
	p = '?symbol=BTCUSDT&limit=1000'
	url = base + q + p

	x = requests.get(url)
	d = x.text
	dd = json.loads(d)
	return dd[::-1]


def avg_price_vol():
	current_trades = current_min_trades()
	starting_time = current_trades[0]['time']
	print(datetime.utcfromtimestamp(starting_time/1000).strftime('%Y-%m-%d %H:%M:%S'))
	price_lst = []
	vol_lst = []
	avg_price = 0.0
	vol = 0.0
	for i,val in enumerate(current_trades):
		t = val['time']
		dif = abs(starting_time-t)
		# print(f'diff: {dif}')
		# print(datetime.utcfromtimestamp(t/1000).strftime('%Y-%m-%d %H:%M:%S'))
		if dif <= 60000:
			price = float(val['price'])
			price_lst.append(price)
			qty = float(val['qty'])
			vol_lst.append(qty)
		if dif > 60000:
			avg_price = mean(price_lst)
			vol = round(sum(vol_lst),2)
			break
		
	return {'price':avg_price, 'vol': vol}


def prep_data(p, v):
	for i in range(500):
		ct = avg_price_vol()
		print(ct)
		current_price = ct['price']
		current_vol = ct['vol']
		global prev_price
		global prev_vol
		# print(f'cp: {current_price}, pp: {prev_price}, cv: {current_vol}, pv: {prev_vol}')
		
		prv_data = f'time,{prev_price},high,low,close,{prev_vol}\n' 
		current_data = f'time,{current_price},high,low,close,{current_vol}'
		print(prv_data+current_data)

		prev_price = current_price
		prev_vol = current_vol
		
		time.sleep(60)

# time,open,high,low,close,volume
# 1502942400,4261.48,4261.48,4261.48,4261.48,1.775183
# 1502942460,4261.48,4261.48,4261.48,4261.48,0
prep_data(1,1)
