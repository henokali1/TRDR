from datetime import datetime

s_prev_pattern={'H-H': {'pattern': 'H-H', 'cntr': 3141}, 'H': {'pattern': 'H', 'cntr': 6112}, 'B': {'pattern': 'B', 'cntr': 12607}, 'H-H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H-H', 'cntr': 103}, 'H-H-H': {'pattern': 'H-H-H', 'cntr': 1494}, 'H-H-H-H': {'pattern': 'H-H-H-H', 'cntr': 757}, 'H-H-H-H-H': {'pattern': 'H-H-H-H-H', 'cntr': 409}, 'H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H', 'cntr': 206}, 'H-H-H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H-H-H', 'cntr': 48}, 'H-H-H-H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H-H-H-H', 'cntr': 31}, 'H-H-H-H-H-H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H-H-H-H-H-H', 'cntr': 6}, 'H-H-H-H-H-H-H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H-H-H-H-H-H-H', 'cntr': 2}, 'H-H-H-H-H-H-H-H-H-H-H-H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H-H-H-H-H-H-H-H-H-H-H-H', 'cntr': 1}, 'H-H-H-H-H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H-H-H-H-H', 'cntr': 11}, 'H-H-H-H-H-H-H-H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H-H-H-H-H-H-H-H', 'cntr': 1}}
s_prev_prev_pattern={'H': {'pattern': 'H', 'cntr': 6344}, 'B': {'pattern': 'B', 'cntr': 6112}, 'S': {'pattern': 'S', 'cntr': 6183}, 'H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H', 'cntr': 186}, 'H-H-H': {'pattern': 'H-H-H', 'cntr': 1575}, 'H-H': {'pattern': 'H-H', 'cntr': 3141}, 'H-H-H-H-H': {'pattern': 'H-H-H-H-H', 'cntr': 400}, 'H-H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H-H', 'cntr': 88}, 'H-H-H-H': {'pattern': 'H-H-H-H', 'cntr': 802}, 'H-H-H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H-H-H', 'cntr': 53}, 'H-H-H-H-H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H-H-H-H-H', 'cntr': 13}, 'H-H-H-H-H-H-H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H-H-H-H-H-H-H', 'cntr': 3}, 'H-H-H-H-H-H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H-H-H-H-H-H', 'cntr': 4}, 'H-H-H-H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H-H-H-H', 'cntr': 23}, 'H-H-H-H-H-H-H-H-H-H-H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H-H-H-H-H-H-H-H-H-H-H', 'cntr': 1}, 'H-H-H-H-H-H-H-H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H-H-H-H-H-H-H-H', 'cntr': 1}}
b_prev_pattern={'H': {'pattern': 'H', 'cntr': 6185}, 'S': {'pattern': 'S', 'cntr': 12358}, 'H-H-H': {'pattern': 'H-H-H', 'cntr': 1639}, 'H-H-H-H': {'pattern': 'H-H-H-H', 'cntr': 808}, 'H-H-H-H-H': {'pattern': 'H-H-H-H-H', 'cntr': 420}, 'H-H': {'pattern': 'H-H', 'cntr': 3185}, 'H-H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H-H', 'cntr': 97}, 'H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H', 'cntr': 176}, 'H-H-H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H-H-H', 'cntr': 45}, 'H-H-H-H-H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H-H-H-H-H', 'cntr': 17}, 'H-H-H-H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H-H-H-H', 'cntr': 17}, 'H-H-H-H-H-H-H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H-H-H-H-H-H-H', 'cntr': 3}, 'H-H-H-H-H-H-H-H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H-H-H-H-H-H-H-H', 'cntr': 1}, 'H-H-H-H-H-H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H-H-H-H-H-H', 'cntr': 4}}
b_prev_prev_pattern={'S': {'pattern': 'S', 'cntr': 6185}, 'H': {'pattern': 'H', 'cntr': 6237}, 'H-H': {'pattern': 'H-H', 'cntr': 3237}, 'B': {'pattern': 'B', 'cntr': 6175}, 'H-H-H': {'pattern': 'H-H-H', 'cntr': 1562}, 'H-H-H-H': {'pattern': 'H-H-H-H', 'cntr': 799}, 'H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H', 'cntr': 199}, 'H-H-H-H-H': {'pattern': 'H-H-H-H-H', 'cntr': 382}, 'H-H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H-H', 'cntr': 87}, 'H-H-H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H-H-H', 'cntr': 39}, 'H-H-H-H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H-H-H-H', 'cntr': 37}, 'H-H-H-H-H-H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H-H-H-H-H-H', 'cntr': 6}, 'H-H-H-H-H-H-H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H-H-H-H-H-H-H', 'cntr': 1}, 'H-H-H-H-H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H-H-H-H-H', 'cntr': 9}}
h_prev_pattern={'H': {'pattern': 'H', 'cntr': 12623}, 'S': {'pattern': 'S', 'cntr': 12571}, 'B': {'pattern': 'B', 'cntr': 12348}, 'H-H': {'pattern': 'H-H', 'cntr': 6297}, 'H-H-H': {'pattern': 'H-H-H', 'cntr': 3163}, 'H-H-H-H': {'pattern': 'H-H-H-H', 'cntr': 1598}, 'H-H-H-H-H': {'pattern': 'H-H-H-H-H', 'cntr': 769}, 'H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H', 'cntr': 387}, 'H-H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H-H', 'cntr': 187}, 'H-H-H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H-H-H', 'cntr': 94}, 'H-H-H-H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H-H-H-H', 'cntr': 46}, 'H-H-H-H-H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H-H-H-H-H', 'cntr': 18}, 'H-H-H-H-H-H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H-H-H-H-H-H', 'cntr': 8}, 'H-H-H-H-H-H-H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H-H-H-H-H-H-H', 'cntr': 3}, 'H-H-H-H-H-H-H-H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H-H-H-H-H-H-H-H', 'cntr': 1}, 'H-H-H-H-H-H-H-H-H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H-H-H-H-H-H-H-H-H', 'cntr': 1}, 'H-H-H-H-H-H-H-H-H-H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H-H-H-H-H-H-H-H-H-H', 'cntr': 1}, 'H-H-H-H-H-H-H-H-H-H-H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H-H-H-H-H-H-H-H-H-H-H', 'cntr': 1}}
h_prev_prev_pattern={'': {'pattern': '', 'cntr': 1}, 'H-H': {'pattern': 'H-H', 'cntr': 6244}, 'H': {'pattern': 'H', 'cntr': 12339}, 'S': {'pattern': 'S', 'cntr': 12561}, 'B': {'pattern': 'B', 'cntr': 12668}, 'H-H-H': {'pattern': 'H-H-H', 'cntr': 3159}, 'H-H-H-H': {'pattern': 'H-H-H-H', 'cntr': 1562}, 'H-H-H-H-H': {'pattern': 'H-H-H-H-H', 'cntr': 816}, 'H-H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H-H', 'cntr': 212}, 'H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H', 'cntr': 384}, 'H-H-H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H-H-H', 'cntr': 95}, 'H-H-H-H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H-H-H-H', 'cntr': 34}, 'H-H-H-H-H-H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H-H-H-H-H-H', 'cntr': 8}, 'H-H-H-H-H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H-H-H-H-H', 'cntr': 24}, 'H-H-H-H-H-H-H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H-H-H-H-H-H-H', 'cntr': 4}, 'H-H-H-H-H-H-H-H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H-H-H-H-H-H-H-H', 'cntr': 2}, 'H-H-H-H-H-H-H-H-H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H-H-H-H-H-H-H-H-H', 'cntr': 1}, 'H-H-H-H-H-H-H-H-H-H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H-H-H-H-H-H-H-H-H-H', 'cntr': 1}, 'H-H-H-H-H-H-H-H-H-H-H-H-H-H-H-H-H': {'pattern': 'H-H-H-H-H-H-H-H-H-H-H-H-H-H-H-H-H', 'cntr': 1}}


def percentage_diff(cp, pp):
	try:
		return (100.0*(cp-pp))/pp
	except:
		return 0.0

def action(c_pd, f_pd):
	if((c_pd < 0) and (f_pd > 0)):
		return 'B'
	if((c_pd > 0) and (f_pd < 0)):
		return 'S'
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


def chunk_data(
		export_file_name,current_price_lst,current_vol_lst,
		price_pd_lst,vol_pd_lst,prev_acts_lst,prev_prev_acts_lst,act_lst,
	):
	r=''
	title = 'currentPrice,currentVolume,pricePd,volPd,prevActs,prevPrevActs,Action\n'
	r += title
	for i in range(len(current_price_lst)):
		if(i <= len(current_price_lst)):
			r += f'{current_price_lst[i]},{current_vol_lst[i]},{price_pd_lst[i]},{vol_pd_lst[i]},{"-".join(list(prev_acts_lst[i]))},{"-".join(list(prev_prev_acts_lst[i]))},{act_lst[i]}\n'
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
	prev_prev_act = 'H'
	prev_act = 'H'

	prev_acts_val = []
	prev_prev_acts_lst = []


	current_price_lst = []
	current_vol_lst = []
	price_pd_lst = []
	vol_pd_lst = []
	act_lst = []
	prev_prev_act_lst = []
	prev_act_lst = []
	prev_acts_lst = []


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

		if prev_act != prev_prev_act:
			prev_prev_acts_lst.append(tuple(prev_acts_val))
			prev_acts_val.clear()
		else:
			prev_prev_acts_lst.append(tuple(prev_acts_val))

		
		prev_acts_val.append(prev_act)
		prev_acts_lst.append(tuple(prev_acts_val))
		


		act = action(current_price_pd, f_pd)


		current_price_lst.append(open_price)
		current_vol_lst.append(volume)
		price_pd_lst.append(current_price_pd)
		vol_pd_lst.append(round(percentage_diff(volume, prev_vol),6))
		act_lst.append(act)
		prev_prev_act_lst.append(prev_prev_act)
		prev_act_lst.append(prev_act)


		prev_prev_act = prev_act
		prev_act = act

		if(i%update == 0):
			print("Remaining:\t",-1*size-i)
	
	chunk_data(
		export_file_name=export_file_name,
		current_price_lst=current_price_lst,
		current_vol_lst=current_vol_lst,
		price_pd_lst=price_pd_lst,
		vol_pd_lst=vol_pd_lst,
		act_lst=act_lst,
		prev_acts_lst=prev_acts_lst,
		prev_prev_acts_lst=prev_prev_acts_lst,
	)


def pattern_ext(file_name):
	with open(file_name,'r') as f:
		rd = f.read()
	spltd = rd.split('\n')
	del spltd[-1]
	del spltd[0]

	h_prev_pattern = {}
	h_prev_prev_pattern = {}
	b_prev_pattern = {}
	b_prev_prev_pattern = {}
	s_prev_pattern = {}
	s_prev_prev_pattern = {}
	
	for row in spltd:
		vals = row.split(',')
		action = vals[-1]
		prevPattern = vals[-3]
		prevPrevPattern = vals[-2]

		if action == 'H':
			if prevPattern in h_prev_pattern:
				h_prev_pattern[prevPattern]['cntr'] = h_prev_pattern[prevPattern]['cntr'] + 1
			else:
				h_prev_pattern[prevPattern] = {'pattern':prevPattern, 'cntr': 1}
			
			if prevPrevPattern in h_prev_prev_pattern:
				h_prev_prev_pattern[prevPrevPattern]['cntr'] = h_prev_prev_pattern[prevPrevPattern]['cntr'] + 1
			else:
				h_prev_prev_pattern[prevPrevPattern] = {'pattern':prevPrevPattern, 'cntr': 1}

		if action == 'B':
			if prevPattern in b_prev_pattern:
				b_prev_pattern[prevPattern]['cntr'] = b_prev_pattern[prevPattern]['cntr'] + 1
			else:
				b_prev_pattern[prevPattern] = {'pattern':prevPattern, 'cntr': 1}
			
			if prevPrevPattern in b_prev_prev_pattern:
				b_prev_prev_pattern[prevPrevPattern]['cntr'] = b_prev_prev_pattern[prevPrevPattern]['cntr'] + 1
			else:
				b_prev_prev_pattern[prevPrevPattern] = {'pattern':prevPrevPattern, 'cntr': 1}
		
		if action == 'S':
			if prevPattern in s_prev_pattern:
				s_prev_pattern[prevPattern]['cntr'] = s_prev_pattern[prevPattern]['cntr'] + 1
			else:
				s_prev_pattern[prevPattern] = {'pattern':prevPattern, 'cntr': 1}
			
			if prevPrevPattern in s_prev_prev_pattern:
				s_prev_prev_pattern[prevPrevPattern]['cntr'] = s_prev_prev_pattern[prevPrevPattern]['cntr'] + 1
			else:
				s_prev_prev_pattern[prevPrevPattern] = {'pattern':prevPrevPattern, 'cntr': 1}

	print('.............................................................................')
	print(h_prev_prev_pattern)
	print('h_prev_prev_pattern')
	print('.............................................................................')

# size = 100000
# update = 10000
# exp_fn = 'v7.csv'

# prepare_dataset(raw_data_file_name='raw_data.csv', export_file_name=exp_fn, size=size, update=update)

# pattern_ext('v7.csv')

cntr = 0
for i in h_prev_pattern:
	if i in s_prev_pattern:
		cntr += 1
print(cntr, len(s_prev_pattern)-cntr)
