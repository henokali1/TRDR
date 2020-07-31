import requests
import ast
import json
import time
from datetime import datetime
from statistics import mean


prev_price = 0.0
prev_vol = 0.0
one_min_ms = 20000
binance_req_delay = 20


def percentage_diff(cp, pp):
	try:
		return (100.0*(cp-pp))/pp
	except:
		return 0.0

def action(c_pd, f_pd):
	if((c_pd < 0) and (f_pd > 0)):
		return 'B'
	elif((c_pd > 0) and (f_pd < 0)):
		return 'S'
	else:
		return 'H'

def priv_price(val):
	sp = val.split(',')
	return float(sp[1])

# def write_csv(val, file_name):
# 	try:
# 		print('Exporting file.....')
# 		with open(file_name, 'w') as the_file:
# 			the_file.write(val)
# 			print(file_name + ' exported')
# 	except:
# 		print("Couldn't export data :'(")


def chunk_data(price_lst, volume_lst, price_pd_lst, volume_pd_lst, price_pd_bn_trades_lst, volume_pd_bn_trades_lst, mins_bn_trade_lst, h_pd_lst, h_price_pd_bn_trades_lst, h_volume_pd_bn_trades_lst, h_mins_bn_trade_lst, act_lst, export_file_name):
	r=''

	title = 'Price,Volume,Price_PD,Volume_PD,Price_PD_bn_Trades,Volume_PD_bn_Trades,Mins_bn_Trade,H_Price_PD,H_Price_PD_bn_Trades,H_Volume_PD_bn_Trades,H_Mins_bn_Trade,Action\n'
	r += title
	for i,val in enumerate(price_pd_lst):
		if(i <= len(price_pd_lst)):
			r += '{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(price_lst[i], volume_lst[i], price_pd_lst[i], volume_pd_lst[i], price_pd_bn_trades_lst[i], volume_pd_bn_trades_lst[i], mins_bn_trade_lst[i], h_pd_lst[i], h_price_pd_bn_trades_lst[i], h_volume_pd_bn_trades_lst[i], h_mins_bn_trade_lst[i], act_lst[i])
	write_csv(r, file_name=export_file_name)


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
		if dif <= one_min_ms:
			price = float(val['price'])
			price_lst.append(price)
			qty = float(val['qty'])
			vol_lst.append(qty)
		if dif > one_min_ms:
			avg_price = round(mean(price_lst), 2)
			vol = sum(vol_lst)
			break
		
	return {'price':avg_price, 'vol': vol}

	
	
def prepare_dataset(raw_data):
	data_sp = raw_data.split('\n')
	print(data_sp)
	price_pd_lst = []
	volume_pd_lst = []
	price_lst = []
	volume_lst = []
	act_lst = []
	price_pd_bn_trades_lst = []
	volume_pd_bn_trades_lst = []
	mins_bn_trade_lst = []
	h_pd_lst = []
	h_price_pd_bn_trades_lst = []
	h_volume_pd_bn_trades_lst = []
	h_mins_bn_trade_lst = []
	priv_trade_price = 0.0
	priv_trade_vol = 0.0
	mins_bn_trade = 0
	priv_trade_ts = 0
	priv_act = ''
	h_priv_trade_price = 0.0
	h_priv_trade_vol = 0.0
	h_priv_trade_ts = 0
	for i, val in enumerate(data_sp):
		sp = val.split(',')
		open_price = float(sp[1])
		volume = float(sp[-1])
		cur_ts = int(sp[0])

		pp = open_price if i == 0 else priv_price(data_sp[i-1])
		pv = volume if i == 0 else float(data_sp[i-1].split(',')[-1])
		cp = open_price
		cv = volume
		c_pd = round(percentage_diff(cp, pp), 4)
		c_vd = round(percentage_diff(cv, pv), 4)
		fp = cp if i == len(data_sp) -1 else priv_price(data_sp[i+1])

		f_pd = percentage_diff(fp, cp)
		act = action(c_pd, f_pd)
		
		if priv_act != act:
			price_pd_bn_trades = round(percentage_diff(cp, priv_trade_price), 4)
			volume_pd_bn_trades = round(percentage_diff(cv, priv_trade_vol), 4)
			mins_bn_trade = int((cur_ts-priv_trade_ts)/60)
			priv_trade_price = cp
			priv_trade_vol = volume
			priv_trade_ts = cur_ts
			priv_act = act
		else:
			price_pd_bn_trades = 0.0
			volume_pd_bn_trades = 0.0
		
		if act == 'H':
			h_pd = round(percentage_diff(cp, pp), 4)
			h_price_pd_bn_trades = round(percentage_diff(cp, h_priv_trade_price), 4)
			h_volume_pd_bn_trades = round(percentage_diff(cv, h_priv_trade_vol), 4)
			h_mins_bn_trade = int((cur_ts-h_priv_trade_ts)/60)
			h_priv_trade_price = cp
			h_priv_trade_vol = volume
			h_priv_trade_ts = cur_ts
		else:
			h_pd = 0.0
			h_price_pd_bn_trades = 0.0
			h_volume_pd_bn_trades = 0.0



		price_pd_lst.append(c_pd)
		volume_pd_lst.append(c_vd)
		price_lst.append(open_price)
		volume_lst.append(volume)
		price_pd_bn_trades_lst.append(price_pd_bn_trades)
		volume_pd_bn_trades_lst.append(volume_pd_bn_trades)
		mins_bn_trade_lst.append(mins_bn_trade)
		h_pd_lst.append(h_pd)
		h_price_pd_bn_trades_lst.append(h_price_pd_bn_trades)
		h_volume_pd_bn_trades_lst.append(h_volume_pd_bn_trades)
		h_mins_bn_trade_lst.append(h_mins_bn_trade)
		act_lst.append(act)
		if(i%update == 0):
			print("Remaining:\t",-1*size-i)
		 
	chunk_data(
		price_lst=price_lst,
		volume_lst=volume_lst,
		price_pd_lst=price_pd_lst,
		volume_pd_lst=volume_pd_lst,
		price_pd_bn_trades_lst=price_pd_bn_trades_lst,
		volume_pd_bn_trades_lst=volume_pd_bn_trades_lst,
		mins_bn_trade_lst=mins_bn_trade_lst,
		h_pd_lst = h_pd_lst,
		h_price_pd_bn_trades_lst = h_price_pd_bn_trades_lst,
		h_volume_pd_bn_trades_lst = h_volume_pd_bn_trades_lst,
		h_mins_bn_trade_lst = h_mins_bn_trade_lst,
		act_lst=act_lst,
		export_file_name=export_file_name,
	)


def prep_data(p, v):
	for i in range(500):
		ct = avg_price_vol()
		print(ct)
		current_price = ct['price']
		current_vol = ct['vol']
		global prev_price
		global prev_vol
		
		prv_data = f'time,{prev_price},high,low,close,{prev_vol}\n' 
		current_data = f'time,{current_price},high,low,close,{current_vol}'
		raw_data = prv_data+current_data
		print(prv_data+current_data)
		# prepare_dataset(raw_data)
		prev_price = current_price
		prev_vol = current_vol
		
		time.sleep(binance_req_delay)

# time,open,high,low,close,volume
# 1502942400,4261.48,4261.48,4261.48,4261.48,1.775183
# 1502942460,4261.48,4261.48,4261.48,4261.48,0
prep_data(1,1)
