from os import listdir
from os.path import isfile, join
raw_dataset_path = 'raw-dataset/'
all_images = [f for f in listdir(raw_dataset_path) if isfile(join(raw_dataset_path, f))]

fns = {}
tbs = []
for i in all_images:
    k=int(i.split('-')[0])
    tbs.append(k)
    fns[k]=i
srtd = sorted(tbs)
imgs_srtd = []
for i in srtd:
    imgs_srtd.append(fns[i])
data=[]
for i in imgs_srtd:
    price=float(i.split('-')[1])
    data.append({'price':price, 'fn':i})

def action(pp, cp, fp):
    if ((cp < pp) and (cp < fp)):
        return 'B'
    elif ((cp > pp) and (cp > fp)):
        return 'S'
    else:
        return 'H'

labeled_data = []
for i,val in enumerate(data):
    if((i==0) or (i==len(data)-1)):
        pass
    else:
        pp = data[i-1]['price']
        cp = val['price']
        fp = data[i+1]['price']
        act = action(pp=pp, cp=cp, fp=fp)
        labeled_data.append({'action':act,'fn':val['fn']})

def jmp(n, d):
    r=[]
    i=0
    while i<=(len(d)-n):
        r.append(d[i])
        i+=n
    return r

nd=jmp(1, labeled_data)

# len(nd)

# !mkdir labeled-data
# !mkdir labeled-data/H
# !mkdir labeled-data/B
# !mkdir labeled-data/S

from shutil import copyfile
for i in nd:
    src = 'raw-dataset/'+i['fn']
    act = i['action']
    if act == 'B':
        dst = 'labeled-data/B/'+i['fn']
    if act == 'S':
        dst = 'labeled-data/S/'+i['fn']
    if act == 'H':
        dst = 'labeled-data/H/'+i['fn']
    copyfile(src, dst)
