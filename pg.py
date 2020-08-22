def action(pp, cp, fp):
	if ((cp < pp) and (cp < fp)):
		return 'B'
	elif ((cp > pp) and (cp > fp)):
		return 'S'
	else:
		return 'H'

# def action(ct, bt, st, cp, bp, pbs):
# 	if ((ct == bt) and (pbs == 'S')):
# 		return 'B'
# 	elif (((ct == st) or (cp < bp)) and (pbs == 'B')):
# 		return 'S'
# 	else:
# 		return 'H'

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
		price_pd_bp_lst,
		trend_lst,
		tread_hist_lst,
		act_lst,
		share_lst,
		fiat_lst,
		starting_amount,
		profitable,
		percentage_gain,
		net_fiat_profit,
		two_trend_hist_lst,
		trend_hist_up_count_lst,
		trend_hist_down_count_lst,
		two_trend_hist_up_count_lst,
		two_trend_hist_down_count_lst,
		nw_act_lst,
		nw_act_patt_lst,
		export_file_name,
		):
	r = f'Price,PricePD,PricePdBP,trend_lst,TrendHist,TrendHistUpCount,TrendHistDownCount,TwoTrendHist,TwoTrendHistUpCount,TwoTrendHistDownCount,PerfectAct,nw_act_lst,nw_act_patt_lst,Share,Fiat,StartingAmount,Profitable,' + \
		f'Percentage Gain,Net Fiat Profit\n,,,,,,,,,,,,,0.0,{starting_amount},{starting_amount},{profitable},{percentage_gain},{net_fiat_profit}\n'

	for i,val in enumerate(price_pd_lst):
		if(i <= len(price_pd_lst)):
			r += f'{price_lst[i]},{price_pd_lst[i]},{price_pd_bp_lst[i]},{trend_lst[i]},{tread_hist_lst[i]},{trend_hist_up_count_lst[i]},{trend_hist_down_count_lst[i]},{two_trend_hist_lst[i]},{two_trend_hist_up_count_lst[i]},{two_trend_hist_down_count_lst[i]},{act_lst[i]},{nw_act_lst[i]},{nw_act_patt_lst[i]},{share_lst[i]},{fiat_lst[i]}\n'
	write_csv(r, file_name=export_file_name)

def prepare_dataset(
		raw_data_file_name,
		size,
		update,
		export_file_name,
		starting_amount,
		bt,st,
		):
	size = -1*size
	fst = True
	with open(raw_data_file_name,'r') as f:
		rd = f.read()

	spltd = rd.split('\n')
	del spltd[-1]
	# del spltd[0]
	data_sp = spltd[size:]

	act = 'H'
	prev_bs = ''
	prev_trend_hist = []
	tread_idx = 0
	prev_share = 0.0
	bp=0.0
	pbs='S'
	prev_fiat = starting_amount
	prev_act = 'H'
	prev_act_idx = 0

	price_pd_lst = []
	price_pd_bp_lst = []
	price_lst = []
	trend_lst = []
	tread_hist_lst = []
	act_lst = []
	share_lst=[]
	fiat_lst=[]
	two_trend_hist_lst=[]
	trend_hist_up_count_lst = []
	trend_hist_down_count_lst= []
	two_trend_hist_up_count_lst = []
	two_trend_hist_down_count_lst = []
	nw_act_lst = []
	nw_act_patt_lst = []
	for i, val in enumerate(data_sp):
		sp = val.split(',')
		open_price = float(sp[1])

		pp = open_price if i == 0 else priv_price(data_sp[i-1])

		cp = open_price
		c_pd = percentage_diff(cp, pp)

		fp = cp if i == len(data_sp) -1 else priv_price(data_sp[i+1])

		if act != 'H':
			tread_idx = i
		
		price_pd_lst.append(c_pd)
		price_pd_bp_lst.append(percentage_diff(cp,bp))
		price_lst.append(open_price)
		trend_lst.append(trend(cp, pp))
		tread_hist_lst.append('-'.join(trend_lst[tread_idx:]))
		trend_hist_up_count_lst.append('-'.join(trend_lst[tread_idx:]).count('U'))
		trend_hist_down_count_lst.append('-'.join(trend_lst[tread_idx:]).count('D'))
		two_trend_hist_lst.append('-'.join(prev_trend_hist + trend_lst[tread_idx:]))
		two_trend_hist_up_count_lst.append('-'.join(prev_trend_hist + trend_lst[tread_idx:]).count('U'))
		two_trend_hist_down_count_lst.append('-'.join(prev_trend_hist + trend_lst[tread_idx:]).count('D'))

		prev_trend_hist = trend_lst[tread_idx:]
		act = action(pp, cp, fp)

		
		ct = trend_lst[-4:]

		# print('ct: ', ct)
		# act = action(ct, bt, st, cp, bp, pbs)
		if fst and (act == 'S'):
			act = 'H'
			fst = False
		if prev_bs == act:
			act = 'H'
		if act != 'H':
			prev_bs = act
		act_lst.append(act)

		nw_act = prev_act+act
		if (nw_act == 'BS') or (nw_act == 'SB'):
			nw_act_lst.append(nw_act[-1])
		else:
			nw_act_lst.append('H')
		nw_act_patt = trend_lst[prev_act_idx:i]
		nw_act_patt_lst.append('-'.join(nw_act_patt))
		if prev_act != act:
			prev_act = act
			prev_act_idx = i

		if(act == 'H'):
			share_lst.append(prev_share)
			fiat_lst.append(prev_fiat)
		if act == 'B':
			prev_share = prev_fiat/cp
			share_lst.append(prev_share)
			fiat_lst.append(0.0)
			prev_fiat = 0.0
			bp=cp
			pbs = 'B'
		if act == 'S':
			prev_fiat = cp*prev_share
			share_lst.append(0.0)
			fiat_lst.append(prev_fiat)
			prev_share = 0.0
			pbs = 'S'
			


		if(i%update == 0):
			print("Remaining:\t",-1*size-i)
	profitable = fiat_lst[-1] > starting_amount if fiat_lst[-1] != 0.0 else share_lst[-1]*cp > starting_amount
	percentage_gain = round((100*fiat_lst[-1]/starting_amount)-100,2) if fiat_lst[-1] != 0 else round((100*share_lst[-1]*cp/starting_amount)-100,2)
	net_fiat_profit = round(fiat_lst[-1]-starting_amount,2) if fiat_lst[-1] != 0.0 else share_lst[-1]*cp - starting_amount

	print(profitable, ': ', percentage_gain, '%')
	# print(nw_act_lst)
	# for i in range(10):
	# 	print(i+1,': ', trend_hist_up_count_lst.count(i+1))
	chunk_data(
			price_lst=price_lst,
			price_pd_lst=price_pd_lst,
			price_pd_bp_lst=price_pd_bp_lst,
			trend_lst=trend_lst,
			tread_hist_lst=tread_hist_lst,
			act_lst=act_lst,
			share_lst=share_lst,
			fiat_lst=fiat_lst,
			starting_amount=starting_amount,
			profitable=profitable,
			percentage_gain = percentage_gain,
			net_fiat_profit=net_fiat_profit,
			two_trend_hist_lst=two_trend_hist_lst,
			trend_hist_up_count_lst=trend_hist_up_count_lst,
			trend_hist_down_count_lst=trend_hist_down_count_lst,
			two_trend_hist_up_count_lst=two_trend_hist_up_count_lst,
			two_trend_hist_down_count_lst=two_trend_hist_down_count_lst,
			nw_act_lst=nw_act_lst,
			nw_act_patt_lst=nw_act_patt_lst,
			export_file_name=export_file_name,
		)


bt=['D','D','D','U']
st=['U','U','D']

# size = 1440*365
size = 100000
update = 10000
starting_amount = 100.0
exp_fn = 'v9-1.csv'

prepare_dataset(
		raw_data_file_name='raw_data.csv',
		export_file_name=exp_fn,
		size=size,
		update=update,
		starting_amount=starting_amount,
		bt=bt,
		st=st
		)
