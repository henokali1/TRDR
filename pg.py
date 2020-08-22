import requests
import ast



def read_file(fn):
	with open(fn,'r') as f:
		rd = f.read()
	sp = rd.split('\n')
	del sp[0]
	del sp[-1]
	return sp

def pay_load_format(val):
	sp = val.split(',')
	payload = {
		"instances": [
			{
				"PricePD": -0.013926689,
				"PricePdBP": 0.019439075,
				"trend_lst": "D",
				"TrendHist": "D-D",
				"TrendHistDownCount": 2,
				"TrendHistUpCount": 0,
				"TwoTrendHist": "D-D-D",
				"TwoTrendHistDownCount": 3,
				"TwoTrendHistUpCount": 0,
				"nw_act_patt_lst": "D"
			}
		]
	}
	
	return(payload)


def pred(payload):
	r = requests.post("http://34.83.91.155:8080/predict", json=payload).text
	# r = requests.post("http://localhost:8080/predict", json=payload).text
	p = ast.literal_eval(r)
	# row_pred = p['predictions'][0]
	# scores = row_pred['scores']
	# classes = row_pred['classes']
	# confid_score = max(scores)
	# pred_index = scores.index(confid_score)
	# prediction = classes[pred_index]
	return r

payload = pay_load_format('d')
a = pred(payload)
print(a)
# def inp_pred():
# 	while 1:
# 		d = input("Data: ")
# 		if (d == 'q' or d == 'Q'):
# 			break
# 		else:
# 			d = d.replace('\n','')
# 			sp = d.split(',')
# 			actual_action = sp[-1]

# 			payload = pay_load_format(d)

# 			pred(payload, actual_action, 3)

# lst = read_file('t.csv')
# wrong = []
# for idx,i in enumerate(lst):
# 	if (idx%100) == 0:
# 		print('Remaining: {}'.format(len(lst)-idx))
# 		w = len(wrong)
# 		t = len(lst)
# 		accuracy = round(100 - (w*100.0)/t, 2)
# 		print("Accuracy: {}%".format(accuracy))
# 	sp = i.split(',')
# 	actual_action = sp[-1]
# 	payload = pay_load_format(i)
# 	prediction = pred(payload)

# 	if (prediction != actual_action):
# 		wrong.append(idx)
# 	# print(prediction == actual_action, actual_action, prediction)



# print(wrong)

# print("Accuracy: {}%".format(accuracy))
