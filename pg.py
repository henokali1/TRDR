import requests
import ast

wrong = []

def read_file(fn):
	with open(fn,'r') as f:
		rd = f.read()
	sp = rd.split('\n')
	del sp[0]
	del sp[-1]
	return sp

def pred(payload, actual_action, idx):
	r = requests.post("http://34.83.91.155:8080/predict", json=payload).text
	p = ast.literal_eval(r)
	row_pred = p['predictions'][0]
	scores = row_pred['scores']
	classes = row_pred['classes']
	confid_score = max(scores)
	pred_index = scores.index(confid_score)
	prediction = classes[pred_index]

	if not (prediction == actual_action):
		wrong.append(idx)
	# print(prediction == actual_action, actual_action, prediction)


lst = read_file('v5-testing-dataset-all.csv')


for i, d in enumerate(lst):
	# d = input("Data: ")
	# if (d == 'q' or d == 'Q'):
	# 	break
	# else:
	d = d.replace('\n','')
	sp = d.split(',')
	actual_action = sp[-1]

	payload = {
		"instances": [
			{
				"Price": float(sp[0]),
				"Volume": float(sp[1]),
				"Price_PD": float(sp[2]),
				"Volume_PD": float(sp[3]),
				"Price_PD_bn_Trades": float(sp[4]),
				"Volume_PD_bn_Trades": float(sp[5]),
				"Mins_bn_Trade": int(sp[6]),
				"H_Price_PD": float(sp[7]),
				"H_Price_PD_bn_Trades": float(sp[8]),
				"H_Volume_PD_bn_Trades": float(sp[9]),
				"H_Mins_bn_Trade": int(sp[10])
			}
		]
	}

	pred(payload, actual_action, i)
	if i%100000 == 0:
		print('Remaining:\t',(1534866 - i))
print(len(wrong))
print(wrong)