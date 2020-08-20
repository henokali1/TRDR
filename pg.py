def action(pp, cp, fp):
	if ((cp < pp) and (cp < fp)):
		return 'B'
	elif ((cp > pp) and (cp > fp)):
		return 'S'
	else:
		return 'H'

def percentage_diff(cp, pp):
	try:
		return (100.0*(cp-pp))/pp
	except:
		return 0.0

def priv_price(val):
	sp = val.split(',')
	return float(sp[1])

def write_csv(val, file_name):
	try:
		with open(file_name, 'w') as the_file:
			the_file.write(val)
			print(file_name + ' exported')
	except:
		print("Couldn't export data :'(")

def trend(cp, pp):
	if cp > pp:
		return "U"
	elif cp < pp:
		return "D"
	else:
		return "N"

def chunk_data(
		price_lst,
		price_pd_lst,
		trend_lst,
		trend_hist_lst,
		act_hist_lst,
		price_pd_tread_lst,
		act_lst,
		export_file_name,
		):
	r = 'Price,PricePD,Trend,TrendHist,ActionHist,price_pd_tread_lst,Action\n'
	for i,val in enumerate(price_pd_lst):
		if(i <= len(price_pd_lst)):
			r += f'{price_lst[i]},{price_pd_lst[i]},{trend_lst[i]},{trend_hist_lst[i]},{act_hist_lst[i]},{price_pd_tread_lst[i]},{act_lst[i]}\n'
	write_csv(r, file_name=export_file_name)

def prepare_dataset(
		raw_data_file_name,
		size,
		update,
		export_file_name,
		starting_amount,
		):
	size = -1*size
	fst = True
	with open(raw_data_file_name,'r') as f:
		rd = f.read()

	spltd = rd.split('\n')
	del spltd[-1]
	# del spltd[0]
	data_sp = spltd[size:]

	prev_exc = 'H'
	trade_idx = 0
	trade_price = 0.0
	bp = 0.0
	balance = starting_amount

	price_pd_lst = []
	price_lst = []
	trend_lst = []
	act_lst = []
	trend_hist_lst = []
	price_pd_tread_lst = []
	act_hist_lst = []
	balance_lst = []
	for i, val in enumerate(data_sp):
		sp = val.split(',')
		open_price = float(sp[1])

		pp = open_price if i == 0 else priv_price(data_sp[i-1])

		cp = open_price
		c_pd = percentage_diff(cp, pp)

		fp = cp if i == len(data_sp) -1 else priv_price(data_sp[i+1])

		
		act = 'H'

		if fst and (act == 'S'):
			act = 'H'
			fst = False

		price_pd_lst.append(c_pd)
		price_lst.append(open_price)
		trend_lst.append(trend(cp, pp))
		trend_hist_lst.append('-'.join(trend_lst[trade_idx:]))
		act_hist_lst.append('-'.join(act_lst[trade_idx-1:]))
		price_pd_tread_lst.append(percentage_diff(cp, trade_price))

		act = 'H'
		if (prev_exc != 'B') and (trend_lst[-4:] == ['D','D','U','U']):
			act = 'B'
			bp = cp
			prev_exc = 'B'
			balance_lst.append(balance)
			# print('Buy: ', cp)
		if (prev_exc == 'B') and ((trend_lst[-3:] == ['U','U','D']) or (cp < bp)):
			act = 'S'
			prev_exc = 'S'
			# print('Sell: ', cp)

		act_lst.append(act)


		if not(act == 'H'):
			trade_idx = i
			trade_price = cp
		if(i%update == 0):
			print("Remaining:\t",-1*size-i)

	chunk_data(
			price_lst=price_lst,
			price_pd_lst=price_pd_lst,
			trend_lst=trend_lst,
			trend_hist_lst=trend_hist_lst,
			act_hist_lst=act_hist_lst,
			price_pd_tread_lst=price_pd_tread_lst,
			act_lst=act_lst,
			export_file_name=export_file_name,
		)


size = 1440*30*6
update = 10000
starting_amount = 100.0
exp_fn = 'v10-1.csv'

prepare_dataset(
		raw_data_file_name='raw_data.csv',
		export_file_name=exp_fn,
		size=size,
		update=update,
		starting_amount=starting_amount,
		)
