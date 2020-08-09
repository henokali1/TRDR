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
	
	
def prepare_dataset(raw_data_file_name, update, export_file_name):
	with open(raw_data_file_name,'r') as f:
		rd = f.read()
	sp = rd.split('\n')[3:-1]
	tot = len(sp)
	r='Time,Price\n'
	for i,ln in enumerate(sp):
		spp = ln.split(',')
		r+=spp[0]+','+spp[16]+'\n'

		if(i%update == 0):
			print("Remaining:\t",tot-i)
	print('Exporting ',export_file_name,'........')
	write_csv(r, file_name=export_file_name)


	
update = 1000

exp_fn = 'aapl'+'.csv'

prepare_dataset(raw_data_file_name='dataset.csv', export_file_name=exp_fn, update=update)
