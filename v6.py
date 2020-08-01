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

def get_prev_vol(val):
	sp = val.split(',')
	return float(sp[-1])

def write_csv(val, file_name):
	try:
		print('Exporting file.....')
		with open(file_name, 'w') as the_file:
			the_file.write(val)
			print(file_name + ' exported')
	except:
		print("Couldn't export data :'(")


def chunk_data(export_file_name,current_price_lst,current_vol_lst,prev_price_lst,prev_vol_lst,price_pd_lst,vol_pd_lst,prev_prev_act_lst,prev_act_lst,prev_price_pd_lst,prev_prev_price_pd_lst,act_lst):
	r=''

	title = 'currentPrice,currentVolume,previousPrice,previousVolume,pricePD,volPD,PrevPrevAct,PrevAct,PrevPricePD,PrevPrevPricePD,Action\n'
	r += title
	for i,val in enumerate(current_price_lst):
		if(i <= len(current_price_lst)):
			r += f'{current_price_lst[i]},{current_vol_lst[i]},{prev_price_lst[i]},{prev_vol_lst[i]},{price_pd_lst[i]},{vol_pd_lst[i]},{prev_prev_act_lst[i]},{prev_act_lst[i]},{prev_price_pd_lst[i]},{prev_prev_price_pd_lst[i]},{act_lst[i]}\n'
	write_csv(r, file_name=export_file_name)
	
	
def prepare_dataset(raw_data_file_name, size, update, export_file_name):
	size = -1*size
	with open(raw_data_file_name,'r') as f:
		rd = f.read()

	spltd = rd.split('\n')
	del spltd[-1]
	del spltd[0]
	data_sp = spltd[size:]

	prev_price = 0.0
	prev_vol = 0.0
	prev_price_pd = 0.0
	prev_prev_price_pd = 0.0
	prev_prev_act = 'H'
	prev_act = 'H'

	current_price_lst = []
	current_vol_lst = []
	prev_price_lst = []
	prev_vol_lst = []
	price_pd_lst = []
	vol_pd_lst = []
	act_lst = []
	prev_prev_act_lst = []
	prev_act_lst = []
	prev_price_pd_lst = []
	prev_prev_price_pd_lst = []


	for i, val in enumerate(data_sp):
		sp = val.split(',')

		open_price = float(sp[1])
		volume = float(sp[-1])
		if(i>0):
			prev_price = priv_price(data_sp[i-1])
			prev_vol = get_prev_vol(data_sp[i-1])
		current_price_pd = round(percentage_diff(open_price, prev_price), 6)
		fp = open_price if i == len(data_sp) -1 else priv_price(data_sp[i+1])
		f_pd = percentage_diff(fp, open_price)

		act = action(current_price_pd, f_pd)


		current_price_lst.append(open_price)
		current_vol_lst.append(volume)
		prev_price_lst.append(prev_price)
		prev_vol_lst.append(prev_vol)
		price_pd_lst.append(current_price_pd)
		vol_pd_lst.append(round(percentage_diff(volume, prev_vol),6))
		act_lst.append(act)
		prev_prev_act_lst.append(prev_prev_act)
		prev_act_lst.append(prev_act)
		prev_price_pd_lst.append(prev_price_pd)
		prev_prev_price_pd_lst.append(prev_prev_price_pd)


		prev_prev_act = prev_act
		prev_prev_price_pd = prev_price_pd
		prev_act = act
		prev_price_pd = current_price_pd

		if(i%update == 0):
			print("Remaining:\t",-1*size-i)
		 
	chunk_data(
		export_file_name=export_file_name,
		current_price_lst=current_price_lst,
		current_vol_lst=current_vol_lst,
		prev_price_lst=prev_price_lst,
		prev_vol_lst=prev_vol_lst,
		price_pd_lst=price_pd_lst,
		vol_pd_lst=vol_pd_lst,
		act_lst=act_lst,
		prev_prev_act_lst=prev_prev_act_lst,
		prev_act_lst=prev_act_lst,
		prev_price_pd_lst=prev_price_pd_lst,
		prev_prev_price_pd_lst=prev_prev_price_pd_lst,
	)

# size = 1534866
# update = int(input('Update: '))

# exp_fn = input('Exprot Dataset Filename: ')+'.csv'
size = 100000
update = 10000
exp_fn = 'v6-training-dataset-100k.csv'

prepare_dataset(raw_data_file_name='raw_data.csv', export_file_name=exp_fn, size=size, update=update)
