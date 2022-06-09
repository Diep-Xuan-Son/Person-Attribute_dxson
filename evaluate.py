import os
import json
import torch
import argparse
from PIL import Image
from torchvision import transforms as T
from net import get_model
import numpy as np
def xnor(lst1, lst2):
    arr_result = []
    for count, i in enumerate(lst1):
        if i == lst2[count] == 0:
            arr_result.append(None)
        elif i == lst2[count] == 1:
            arr_result.append(1)
        elif i != lst2[count]:
            arr_result.append(0)
    return arr_result
with open('./doc/final_label.json', 'r', encoding = 'utf-8') as labels:
    label = list(json.load(labels).values())
label.sort()
for name in ['Duke', 'Market', 'Mydata_1', 'Mydata_2']:
    with open(f'./doc/final_{name}.json', 'r', encoding = 'utf-8') as f:
        globals()[f'att_{name}'] = json.load(f)
        globals()[name] = dict()
        for i in globals()[f'att_{name}']:
            num_arr = []
            for j in label:
                if j not in globals()[f'att_{name}'][i].keys():
                    num_arr.append(0)
                else:
                    num_arr.append(globals()[f'att_{name}'][i][j])
            globals()[name][i] = num_arr
######################################################################
# Settings
# ---------
transforms = T.Compose([
    T.Resize(size=(288, 144)),
    T.ToTensor(),
    T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])
use_id = False
######################################################################
# Argument
# ---------
model_name = '{}_nfc_id'.format('resnet50') if use_id else '{}_nfc'.format('resnet50')
# num_label, num_id = num_cls_dict[args.dataset], num_ids_dict[args.dataset]
# print(num_label, num_id)
num_label, num_id = len(label), 1
# Model and Data
# ---------
def load_network(network):
    save_path = os.path.join('./checkpoints', 'person.pth')
    network.load_state_dict(torch.load(save_path))
    print('Resume model from {}'.format(save_path))
    return network
def load_image(path):
    src = Image.open(path)
    src = transforms(src)
    src = src.unsqueeze(dim=0).cuda()
    return src
print(num_label, num_id)
model = get_model(model_name, num_label, use_id=False, num_id=num_id)
model = load_network(model)
model.eval()
model = model.cuda()
num = 0
result = np.empty((0,len(label)), int)
for root, dirs, files in os.walk('/content/dataset'):
    for file in files:
        if file.endswith('.jpg'):
            num += 1
            # print(root, file)
            name_data = root.split('/')[3]
            if num % 100 == 0:
                # print(result)
                print(num)
            image_path = os.path.join(root, file)
            ids = file.split('_')[0].rjust(4, '0')
            src = load_image(image_path)
            out = model.forward(src)
            pred = torch.gt(out, torch.ones_like(out)/2 )  # threshold=0.5
            pred = pred.tolist()[0]
            # any(pred[inter] = 1 if i else pred[inter] = 0 for inter, i in enumerate(pred))
            pred = [1 if c else 0 for c in pred]
            # compare = np.array(globals()[name_data][ids])^pred^1
            compare = np.array(xnor(pred, globals()[name_data][ids]))
            result = np.vstack ((result, compare) )
np.save("result.npy", result)
row, colum = result.shape
for count, i in enumerate(label):
    check = result[:, count]
    number = 0
    total = 0
    for j in check:
        if j == 1:
            number += 1
            total += 1
        elif j == 0:
            total += 1
    print(i, round(number/total, 4))