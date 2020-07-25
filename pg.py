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

def write_csv(val):
	with open('formatted_data.csv', 'a') as the_file:
		the_file.write(val)



def format_data(data_sp):
	r = ''
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

		r = '{},{},{},{},{},{}\n'.format(timestamp, tim, open_price, volume, c_pd, act)
		write_csv(r)
		if(i%1000 == 0):
			print("Remaining:\t",500000-i)
	

data = """1595461020,9502.93,9510.04,9502.57,9509.85,23.867749
1595461080,9509.92,9514.48,9509.29,9512.66,39.05067
1595461140,9512.66,9513.21,9512.63,9513.2,23.894138
1595461200,9513.2,9513.91,9511.73,9512.28,34.32692"""

with open('raw_data.csv','r') as f:
	rd = f.read()
	print(len(rd))

sp = rd.split('\n')
frmt = sp[-500000:]

format_data(frmt)
# write_csv(data)
