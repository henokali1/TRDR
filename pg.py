from datetime import datetime

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
	if((c_pd < 0) and (f_pd > 0)):
		return 'B'
	elif((c_pd > 0) and (f_pd < 0)):
		return 'S'
	else:
		return 'H'

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

def chunk_data(time_lst, pd_lst, price_lst, act_lst, late_act, pts_lst, ptf_lst, ats_lst, atf_lst, late_trade_pd_lst, nw_trd_act_lst, nnpd, export_file_name):
	r=''

	title = 'Time,Price,Pd,PerfectAction,LateAction,pts_lst,ptf_lst,ats_lst,atf_lst,late_trade_pd_lst,nw_trd_act_lst,nnpd\n'
	r += title
	for i,val in enumerate(pd_lst):
		if(i <= len(pd_lst)):
			r += f'{time_lst[i]},{price_lst[i]},{pd_lst[i]},{act_lst[i]},{late_act[i]},{pts_lst[i]},{ptf_lst[i]},{ats_lst[i]},{atf_lst[i]},{late_trade_pd_lst[i]},{nw_trd_act_lst[i]},{nnpd[i]}\n'
	write_csv(r, file_name=export_file_name)
	
	
def prepare_dataset(raw_data_file_name, size, update, export_file_name, starting_amonunt):
	size = -1*size
	with open(raw_data_file_name,'r') as f:
		rd = f.read()

	spltd = rd.split('\n')
	del spltd[-1]
	del spltd[0]
	data_sp = spltd[size:]

	pd_lst = []
	price_lst = []
	act_lst = []
	time_lst = []
	prev_act = ''
	first_time = True
	for i, val in enumerate(data_sp):
		sp = val.split(',')
		open_price = float(sp[1])
		tm = sp[0]
		pp = open_price if i == 0 else priv_price(data_sp[i-1])

		cp = open_price
		c_pd = percentage_diff(cp, pp)

		fp = cp if i == len(data_sp) -1 else priv_price(data_sp[i+1])

		f_pd = percentage_diff(fp, cp)
		act = action(c_pd, f_pd)

		time_lst.append(tm)
		pd_lst.append(c_pd)
		price_lst.append(open_price)
		if (act=="B") or (act=="S"):
			if act != prev_act:
				prev_act = act
			else:
				act = "H"
		if first_time and act == 'S':
			act = 'H'
		if first_time and act == 'B':
			first_time = False
		act_lst.append(act)
		if(i%update == 0):
			print("Remaining:\t",-1*size-i)
	late_act = ['H'] + act_lst[:-1]
	pts_lst=[]
	ptf_lst=[]
	ats_lst=[]
	atf_lst=[]
	fiat = starting_amonunt
	share = 0.0
	for i,val in enumerate(act_lst):
		if val == 'B':
			share = fiat/price_lst[i]
			fiat=0.0
		if val == 'S':
			fiat = share*price_lst[i]
			share=0.0

		pts_lst.append(share)
		ptf_lst.append(fiat)


	fiat_late = starting_amonunt
	share_late = 0.0
	for i,val in enumerate(late_act):
		if val == 'B':
			share_late = fiat_late/price_lst[i]
			fiat_late=0.0
		if val == 'S':
			fiat_late = share_late*price_lst[i]
			share_late=0.0


		ats_lst.append(share_late)
		atf_lst.append(fiat_late)

	late_trade_pd_lst = []
	prev_late_price = 0.0
	for i in range(len(atf_lst)):
		if atf_lst[i] != 0:
			late_pd = percentage_diff(atf_lst[i],prev_late_price)
			prev_late_price = late_pd
		else:
			late_pd = percentage_diff(ats_lst[i]*price_lst[i],prev_late_price)
			prev_late_price = ats_lst[i]*price_lst[i]
		late_trade_pd_lst.append(prev_late_price)
	
	nw_trd_act_pd_lst = []
	nw_trd_act_lst = []
	buy_price = 0.0
	sell_price = 0.0
	nw_pd = 0.0
	
	for i,val in enumerate(late_act):
		if ((val == 'B') and (act_lst[i-1] == 'B') and (act_lst[i] == 'H')):
			new_act = 'B'
			buy_idx = i
			buy_price = price_lst[i]
			nw_pd = 0.0
		elif ((val == 'S') and (act_lst[i-1] == 'S') and (act_lst[i] == 'H')):
			sell_price = price_lst[i]
			nw_pd = percentage_diff(sell_price, buy_price)
			if nw_pd <= 0:
				nw_pd=0.0
			else:
				new_act = 'S'
		else:
			new_act = 'H'
			nw_pd = 0.0
		nw_trd_act_lst.append(new_act)
		nw_trd_act_pd_lst.append(nw_pd)


	s=0.0
	plst=[]
	nlst = []
	for idx,i in enumerate(nw_trd_act_pd_lst):
		val = i
		if i == 'B':
			buy_idx = idx			
		if i>0:
			plst.append(i)
			s+=i
		else:
			nw_trd_act_lst[buy_idx] = 'H'
			nlst.append(i)
			



	nl=[]
	pbi = 0
	pwb = False
	for idx,val in enumerate(nw_trd_act_lst):
		nl.append(val)
		if (val == 'B') and (pwb == False):
			pbi = idx
			pwb = True
		if (val == 'B') and (pwb == True):
			nl[pbi] = 'H'
			pbi = idx
			pwb = True
		if (val == 'S') and (pwb == True):
			pwb = False

	nnl=[]
	pbs = 'H'
	psi = 0
	for i,val in enumerate(nl):
		nnl.append(val)
		c = val
		p = pbs

		if ((c == 'B') and (p == 'B')):
			pbs = 'B'
		if ((c == 'B') and (p == 'S')):
			pbs = 'B'
		
		if ((c == 'S') and (p == 'B')):
			pbs = 'S'
			psi=i
		if ((c == 'S') and (p == 'S')):
			pbs='S'
			nnl[psi]='H'
			psi=i
		if c in 'BS':
			pbs=c
	
	nns=0.0
	nnpd=[]
	nnpp = 0.0
	nncp = 0.0
	for i,val in enumerate(nnl):
		av = 0.0
		if val == 'B':
			nnpp=price_lst[i]
		elif val == 'S':
			nncp=price_lst[i]
			av = (percentage_diff(nncp,nnpp))
		else:
			av = 0.0
		nnpd.append(av)

	print('NN +ve sum: ', sum(nnpd))

	



	chunk_data(
			time_lst=time_lst, pd_lst=pd_lst,
			price_lst=price_lst, act_lst=act_lst,
			late_act=late_act,pts_lst=pts_lst,
			ptf_lst=ptf_lst, ats_lst=ats_lst,
			atf_lst=atf_lst, late_trade_pd_lst=late_trade_pd_lst,
			nw_trd_act_lst=nnl,nnpd=nnpd,export_file_name=export_file_name,
			)


size = 100000
# size = 50
days = 10
# size = 60*24*days
update = 10000
starting_amonunt = 100.0
exp_fn = 'v8.csv'
prepare_dataset(raw_data_file_name='raw_data.csv', export_file_name=exp_fn, size=size, update=update, starting_amonunt=starting_amonunt)
