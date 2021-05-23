def write_csv(val, file_name):
	try:
		with open(file_name, 'w') as the_file:
			the_file.write(val)
			print(file_name + ' exported')
	except:
		print("Couldn't export data :'(")


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
