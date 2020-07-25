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
	try:
		with open(file_name, 'w') as the_file:
			the_file.write(val)
			print(file_name + ' exported')
	except:
		print("Couldn't export data :'(")

def chunk_data(pd_lst, price_lst, act_lst, volume_lst, export_file_name):
	r=''

	title = 'Price,' + 'Volume,' + 'Pd' + ',Action\n'
	r += title
	for i,val in enumerate(pd_lst):
		if(i <= len(pd_lst)):
			r += '{},{},{},{}\n'.format(price_lst[i], volume_lst[i], pd_lst[i], act_lst[i])
	write_csv(r, file_name=export_file_name)
	
	
def prepare_dataset(raw_data_file_name, size, update, export_file_name):
	size = -1*size
	with open(raw_data_file_name,'r') as f:
		rd = f.read()

	spltd = rd.split('\n')
	del spltd[-1]
	# del spltd[0]
	data_sp = spltd[size:]

	pd_lst = []
	price_lst = []
	volume_lst = []
	act_lst = []
	for i, val in enumerate(data_sp):
		sp = val.split(',')
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
		act_lst.append(act)
		if(i%update == 0):
			print("Remaining:\t",-1*size-i)
	chunk_data(pd_lst=pd_lst, price_lst=price_lst, act_lst=act_lst, volume_lst=volume_lst, export_file_name=export_file_name)

size = 1534866
update = int(input('Update: '))

exp_fn = input('Exprot Dataset Filename: ')+'.csv'

prepare_dataset(raw_data_file_name='raw_data.csv', export_file_name=exp_fn, size=size, update=update)
