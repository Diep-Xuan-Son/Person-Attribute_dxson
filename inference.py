import os
import json
import torch
import argparse
from PIL import Image
from torchvision import transforms as T
from net import get_model
import time
import numpy as np
import matplotlib.pyplot as plt
import cv2
import pandas as pd
def key_sort(lst):
    return int(lst[0])
with open('./doc1/data_duke_market.json', 'r') as labels:
    label = json.load(labels)["label"]
    # label= list(label.values())
label.sort()
######################################################################
# Settings
# ---------
dataset_dict = {
    'market'  :  'Market-1501',
    'duke'  :  'DukeMTMC-reID',
}
num_cls_dict = { 'market':30, 'duke':23 }
num_ids_dict = { 'market':751, 'duke':702 }
# with open('./doc/final_label.json', 'r') as f:
#     data = [i.replace('\n', '') for i in f.readlines() if i != '']
#     num_label = len(data)
num_label = len(label)
num_id = 250
transforms = T.Compose([
    T.Resize(size=(288, 144)),
    T.ToTensor(),
    T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

######################################################################
# Argument
# ---------
parser = argparse.ArgumentParser()
parser.add_argument('--image_path', default='./test_sample/1.jpg', help='Path to test image')
parser.add_argument('--dataset', default='market', type=str, help='dataset')
parser.add_argument('--backbone', default='mobilenet_v2', type=str, help='model')
parser.add_argument('--use-id', action='store_true', help='use identity loss')
args = parser.parse_args()
backbone = args.backbone
print(args)
assert args.dataset in ['market', 'duke']
assert args.backbone in ['resnet50', 'resnet34', 'resnet18', 'densenet121', 'mobilenet_v2']
model_name = '{}_nfc_id'.format(args.backbone) if args.use_id else '{}_nfc'.format(args.backbone)
# num_label, num_id = num_cls_dict[args.dataset], num_ids_dict[args.dataset]
# print(num_label, num_id)
# torch.load(os.path.join('./checkpoints', 'my_weights.pth'))
######################################################################
# Model and Data
# ---------
def load_network(network):
    save_path = os.path.join('./checkpoints/old', 'data_duke_market_80epoch.pth')
    network.load_state_dict(torch.load(save_path))
    print('Resume model from {}'.format(save_path))
    return network

def load_image(path):
    src = Image.open(path)
    src = transforms(src)
    if torch.cuda.is_available():
        src = src.unsqueeze(dim=0).cuda()
    else:
        src = src.unsqueeze(dim=0)
    return src

print(num_label, num_id)
model = get_model(backbone, num_label, use_id=args.use_id, num_id=num_id)
model = load_network(model)
model.eval()
if torch.cuda.is_available():
    model = model.cuda()

inter = 0
arr_num = []
for root, dirs, files in os.walk('/content/drive/MyDrive/BriefCam/dataset_seg/13_04_2022/13_04_2022'):
    for file in files:
        if file.endswith(('.jpg', '.JPG')):
            t1 = time.time()
            inter += 1
            # print(os.path.join(root, file))
            if inter %100 ==0:
                print(f'{inter} images was procced!')
            src = load_image(os.path.join(root, file))
            image = cv2.imread(os.path.join(root, file))
            # ids = file.split('.')[0]
            ids = root.split('/')[8][4:]
            if not args.use_id:
                out = model.forward(src)
            else:
                out, _ = model.forward(src)
            pred = torch.gt(out, torch.ones_like(out)*0.7 )  # threshold=0.5
            pred = pred.tolist()[0]
            print(time.time()-t1)
            predict= list([1 if bol else None for bol in pred])
            predict.insert(0, ids.rjust(4, '0'))
            arr_num.append(predict)
arr_num.sort(key = key_sort)
arr_result = np.array(arr_num)
label.insert(0,'ids')
print(label)
df = pd.DataFrame(arr_result,columns=label)
df.to_excel('/content/dict_noseg.xlsx')
            # for index, i in enumerate(pred):
            #     if label[index] == 'gender' and i:
            #         att.append('Female')
            #     elif label[index] == 'gender' and not i:
            #         att.append('Male')
            #     elif label[index] == 'hair' and i:
            #         att.append('Long hair')
            #     elif label[index] == 'hair' and not i:
            #         att.append('Short hair')
            #     elif i:
            #         att.append(label[index])
            # cv2.imwrite(os.path.join('D:/WORKIT/Person-Attribute-Recognition-MarketDuke/result', '_'.join(att)+ '_'+str(inter) + '.jpg'), image)

