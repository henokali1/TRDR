import requests
import ast


def action(pp, cp, fp):
	if ((cp < pp) and (cp < fp)):
		return 'B'
	elif ((cp > pp) and (cp > fp)):
		return 'S'
	else:
		return 'H'


# def action(ct, ft):
# 	if (ct == 'D') and (ft == 'U'):
# 		return 'B'
# 	elif (ct == 'U') and (ft == 'D'):
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
		trend_lst,
		act_lst,
		share_lst,
		fiat_lst,
		starting_amount,
		profitable,
		percentage_gain,
		net_fiat_profit,
		export_file_name,
		):
	r = f'Price,PricePD,Trend,PerfectAction,Share,Fiat,StartingAmount,Profitable,Percentage Gain,Net Fiat Profit\n' + \
		f',,,,0.0,{starting_amount},{starting_amount},{profitable},' + \
		f'{percentage_gain},{net_fiat_profit}\n'

	for i in range(len((price_pd_lst))):
		if(i <= len(price_pd_lst)):
			r += f'{price_lst[i]},{price_pd_lst[i]},{trend_lst[i]},' + \
			f'{act_lst[i]},' + \
			f'{share_lst[i]},{fiat_lst[i]}\n'
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

	act = 'H'
	prev_bs = ''
	prev_share = 0.0
	prev_fiat = starting_amount
	
	psi=0
	pbi=0

	price_pd_lst = []
	price_lst = []
	trend_lst = []
	act_lst = []
	share_lst=[]
	fiat_lst=[]
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

		act = action(pp, cp, fp)
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
			trend_lst=trend_lst,
			act_lst=act_lst,
			share_lst=share_lst,
			fiat_lst=fiat_lst,
			starting_amount=starting_amount,
			profitable=profitable,
			percentage_gain = percentage_gain,
			net_fiat_profit=net_fiat_profit,
			export_file_name=export_file_name,
		)


# size = 1440*1
size = 50
update = 10000
starting_amount = 100.0
exp_fn = 'v10.csv'

prepare_dataset(
		raw_data_file_name='raw_data.csv',
		export_file_name=exp_fn,
		size=size,
		update=update,
		starting_amount=starting_amount,
		)
