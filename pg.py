import requests
import ast


# def action(pp, cp, fp):
# 	if ((cp < pp) and (cp < fp)):
# 		return 'B'
# 	elif ((cp > pp) and (cp > fp)):
# 		return 'S'
# 	else:
# 		return 'H'


def action(buy, sell, trend_lst):
	for i in buy:
		b_patt = '-'.join(trend_lst[1 + (-1*len(i)):])
		s_patt = '-'.join(trend_lst[1 + (-1*len(i)):])
		b_comp = (i == b_patt)
		s_comp = (i == s_patt)
		if b_comp:
			return 'B'
		if s_comp:
			return 'S'
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
		act_lst,
		share_lst,
		fiat_lst,
		starting_amount,
		profitable,
		percentage_gain,
		net_fiat_profit,
		patt_one_lst,
		patt_two_lst,
		export_file_name,
		):
	r = f'Price,PricePD,Trend,PerfectAction,patt_one_lst,patt_two_lst,Share,Fiat,StartingAmount,Profitable,Percentage Gain,Net Fiat Profit\n' + \
		f',,,,,,0.0,{starting_amount},{starting_amount},{profitable},' + \
		f'{percentage_gain},{net_fiat_profit}\n'

	for i in range(len((price_pd_lst))):
		if(i <= len(price_pd_lst)):
			r += f'{price_lst[i]},{price_pd_lst[i]},{trend_lst[i]},{act_lst[i]},' + \
			f'{patt_one_lst[i]},{patt_two_lst[i]},{share_lst[i]},{fiat_lst[i]}\n'
	write_csv(r, file_name=export_file_name)

def prepare_dataset(
		raw_data_file_name,
		size,
		update,
		export_file_name,
		starting_amount,
		buy_patt_lst,
		sell_patt_lst,
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
	prev_share = 0.0
	prev_fiat = starting_amount
	
	psi=0
	pbi=0
	bp_cntr={}
	sp_cntr={}

	price_pd_lst = []
	price_lst = []
	trend_lst = []
	act_lst = []
	share_lst=[]
	fiat_lst=[]
	patt_one_lst=[]
	patt_two_lst=[]
	for i, val in enumerate(data_sp):
		sp = val.split(',')
		open_price = float(sp[1])

		pp = open_price if i == 0 else priv_price(data_sp[i-1])

		cp = open_price
		c_pd = percentage_diff(cp, pp)

		fp = cp if i == len(data_sp) -1 else priv_price(data_sp[i+1])

		
		price_pd_lst.append(c_pd)
		price_lst.append(open_price)
		trend_lst.append(trend(cp, pp))

		act = action(buy_patt_lst, sell_patt_lst, trend_lst)
		if fst and (act == 'S'):
			act = 'H'
			fst = False
		if prev_bs == act:
			act = 'H'
		if act != 'H':
			prev_bs = act
		act_lst.append(act)

		if(act == 'H'):
			share_lst.append(prev_share)
			fiat_lst.append(prev_fiat)
		if act == 'B':
			prev_share = prev_fiat/cp
			share_lst.append(prev_share)
			fiat_lst.append(0.0)
			prev_fiat = 0.0
			
		if act == 'S':
			prev_fiat = cp*prev_share
			share_lst.append(0.0)
			fiat_lst.append(prev_fiat)
			prev_share = 0.0    


		if act == 'B':
			po='-'.join(trend_lst[psi:i])
			pt='-'.join(trend_lst[pbi:psi])
			pot=pt+'-'+po
			if pot in bp_cntr:
				bp_cntr[pot] += 1
			else:
				bp_cntr[pot] = 1
			pbi=i
		if act == 'S':
			po='-'.join(trend_lst[pbi:i])
			pt='-'.join(trend_lst[psi:pbi])
			pot=pt+'-'+po
			if pot in sp_cntr:
				sp_cntr[pot] += 1
			else:
				sp_cntr[pot] = 1
			psi=i
		if act == 'H':
			po='-'
			pt='-'
		patt_one_lst.append(po)
		patt_two_lst.append(pt)


		# current_patt = '-'.join(trend_lst[i-3:i])
		# print(current_patt)
		# bp1 = 'U:D'.replace(':','-')
		# print(pb1 == )
		
		

		if(i%update == 0):
			print("Remaining:\t",-1*size-i)
	profitable = fiat_lst[-1] > starting_amount if fiat_lst[-1] != 0.0 else share_lst[-1]*cp > starting_amount
	percentage_gain = round((100*fiat_lst[-1]/starting_amount)-100,2) if fiat_lst[-1] != 0 else round((100*share_lst[-1]*cp/starting_amount)-100,2)
	net_fiat_profit = round(fiat_lst[-1]-starting_amount,2) if fiat_lst[-1] != 0.0 else share_lst[-1]*cp - starting_amount

	print('profitable: ', f'{round(percentage_gain,2)}%', f'${int(net_fiat_profit)}') if profitable else print('not profitable: ', percentage_gain, '%')
	# bp_cntr_srtd=sorted(bp_cntr.items(), key=lambda x: x[1], reverse=True)
	# sp_cntr_srtd=sorted(sp_cntr.items(), key=lambda x: x[1], reverse=True)


	# write_csv(str(bp_cntr_srtd), 'v10-buy-count.txt')
	# write_csv(str(sp_cntr_srtd), 'v10-sell-count.txt')


	# chunk_data(
	# 		price_lst=price_lst,
	# 		price_pd_lst=price_pd_lst,
	# 		trend_lst=trend_lst,
	# 		act_lst=act_lst,
	# 		share_lst=share_lst,
	# 		fiat_lst=fiat_lst,
	# 		starting_amount=starting_amount,
	# 		profitable=profitable,
	# 		percentage_gain = percentage_gain,
	# 		net_fiat_profit=net_fiat_profit,
	# 		patt_one_lst=patt_one_lst,
	# 		patt_two_lst=patt_two_lst,
	# 		export_file_name=export_file_name,
	# 	)

buy_patt_lst = ['D-U']
sell_patt_lst = ['U-D']
# size = in
# t(1440*365*2.7)
size = 1440*30*12
update = 100000
starting_amount = 100.0
exp_fn = 'v10.csv'

prepare_dataset(
		raw_data_file_name='raw_data.csv',
		export_file_name=exp_fn,
		size=size,
		update=update,
		starting_amount=starting_amount,
		buy_patt_lst=buy_patt_lst,
		sell_patt_lst=sell_patt_lst,
		)
