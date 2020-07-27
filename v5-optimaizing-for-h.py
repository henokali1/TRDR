from datetime import datetime
import inflect
p = inflect.engine()

def time_price(val):
	ts = int(str(val[0])[:-3])
	td = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	tim = td.split(' ')[1]
	price = val[1]
	return {'time': tim, 'price': price}
def timestamp_to_time(val):
	ts = int(val)
	td = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	tim = td.split(' ')[1]
	return(tim[:-3])

def percentage_diff(cp, pp):
	try:
		return (100.0*(cp-pp))/pp
	except:
		return 0.0

def action(c_pd, f_pd):
	if((c_pd < 0) and (f_pd < 0)):
		return 'H'
	if((c_pd < 0) and (f_pd > 0)):
		return 'B'
	if((c_pd > 0) and (f_pd < 0)):
		return 'S'
	if((c_pd > 0) and (f_pd > 0)):
		return 'H'
	else:
		return 'H'

def priv_price(val):
	sp = val.split(',')
	return float(sp[1])

def write_csv(val, file_name):
	try:
		print('Exporting file.....')
		with open(file_name, 'w') as the_file:
			the_file.write(val)
			print(file_name + ' exported')
	except:
		print("Couldn't export data :'(")


def chunk_data(price_lst, volume_lst, price_pd_lst, volume_pd_lst, price_pd_bn_trades_lst, volume_pd_bn_trades_lst, mins_bn_trade_lst, h_pd_lst, h_price_pd_bn_trades_lst, h_volume_pd_bn_trades_lst, h_mins_bn_trade_lst, act_lst, export_file_name):
	r=''

	title = 'Price,Volume,Price_PD,Volume_PD,Price_PD_bn_Trades,Volume_PD_bn_Trades,Mins_bn_Trade,H_Price_PD,H_Price_PD_bn_Trades,H_Volume_PD_bn_Trades,H_Mins_bn_Trade,Action\n'
	r += title
	for i,val in enumerate(price_pd_lst):
		if(i <= len(price_pd_lst)):
			r += '{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(price_lst[i], volume_lst[i], price_pd_lst[i], volume_pd_lst[i], price_pd_bn_trades_lst[i], volume_pd_bn_trades_lst[i], mins_bn_trade_lst[i], h_pd_lst[i], h_price_pd_bn_trades_lst[i], h_volume_pd_bn_trades_lst[i], h_mins_bn_trade_lst[i], act_lst[i])
	write_csv(r, file_name=export_file_name)
	
	
def prepare_dataset(raw_data_file_name, size, update, export_file_name):
	size = -1*size
	with open(raw_data_file_name,'r') as f:
		rd = f.read()

	spltd = rd.split('\n')
	del spltd[-1]
	del spltd[0]
	data_sp = spltd[size:]

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

# size = 1534866
# update = int(input('Update: '))

# exp_fn = input('Exprot Dataset Filename: ')+'.csv'
size = 150000
update = 10000
exp_fn = 'v5-testing-dataset.csv'

prepare_dataset(raw_data_file_name='raw_data.csv', export_file_name=exp_fn, size=size, update=update)
