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
    return (100.0*(cp-pp))/pp

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
	with open(file_name, 'w') as the_file:
		the_file.write(val)

def chunk_data(pd_lst, price_lst, act_lst, volume_lst, tim_lst, chunk, export_file_name):
	r=''
	chunk_title_lst = [p.ordinal(i+1) for i in range(chunk)]
	chunk_title_str = ','.join(chunk_title_lst)

	title = 'Time,' + 'Price,' + 'Volume,' + chunk_title_str + ',Action\n'
	r += title
	for i,val in enumerate(pd_lst):
		if((i+chunk) <= len(pd_lst)):
			pdl = pd_lst[i:i+chunk]
			pd_lst_str = ','.join(str(v) for v in pdl)
			r += '{},{},{},{},{}\n'.format(tim_lst[i+chunk-1], price_lst[i+chunk-1], volume_lst[i+chunk-1], pd_lst_str, act_lst[i+chunk-1])
	write_csv(r, file_name=export_file_name)
	
	
def prepare_dataset(raw_data_file_name, size, update, chunk, export_file_name):
	size = -1*size - chunk + 1
	with open(raw_data_file_name,'r') as f:
		rd = f.read()

	spltd = rd.split('\n')
	del spltd[-1]
	data_sp = spltd[size:]

	pd_lst = []
	price_lst = []
	volume_lst = []
	tim_lst = []
	act_lst = []
	for i, val in enumerate(data_sp):
		sp = val.split(',')
		timestamp = sp[0]
		tim = timestamp_to_time(timestamp)
		open_price = float(sp[1])
		volume = float(sp[-1])

		pp = open_price if i == 0 else priv_price(data_sp[i-1])

		cp = open_price
		c_pd = percentage_diff(cp, pp)

		fp = cp if i == len(data_sp) -1 else priv_price(data_sp[i+1])

		f_pd = percentage_diff(fp, cp)
		act = action(c_pd, f_pd)

		pd_lst.append(c_pd)
		price_lst.append(open_price)
		volume_lst.append(volume)
		tim_lst.append(tim)
		act_lst.append(act)
		if(i%update == 0):
			print("Remaining:\t",-1*size-i)
	chunk_data(pd_lst=pd_lst, price_lst=price_lst, act_lst=act_lst, volume_lst=volume_lst, tim_lst=tim_lst, chunk=chunk, export_file_name=export_file_name)

exp_fn = 'ttformatted_data_v2.csv'
prepare_dataset(raw_data_file_name='raw_data.csv', export_file_name=exp_fn, size=10, update=10, chunk=10)