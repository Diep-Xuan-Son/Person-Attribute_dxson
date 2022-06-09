import os
from PIL import Image
import torch
from torch.utils import data
import numpy as np
from torchvision import transforms as T
import json
# from import_myData import import_attribute, import_nodistractors
def load_data(path):
    with open(path, 'r') as f:
        data = json.load(f)
        return data['train_img'], data['test_img'], data['train_att'], data['test_att'], data['label']
class Train_Dataset(data.Dataset):

    def __init__(self, data_dir, transforms=None, train_val='train' ):
        train, query, train_attr, test_attr, self.label = load_data(data_dir)
        self.num_ids = len(train['ids'])
        self.num_labels = len(self.label)

        # distribution:每个属性的正样本占比
        distribution = np.zeros(self.num_labels)
        for k, v in train_attr.items():
            distribution += np.array(v)
        self.distribution = distribution / len(train_attr)

        if train_val == 'train':
            self.train_data = train['data']
            self.train_ids = train['ids']
            self.train_attr = train_attr
        elif train_val == 'query':
            self.train_data = query['data']
            self.train_ids = query['ids']
            self.train_attr = test_attr
        else:
            print('Input should only be train or val')

        self.num_ids = len(self.train_ids)

        if transforms is None:
            if train_val == 'train':
                self.transforms = T.Compose([
                    T.Resize(size=(288, 144)),
                    T.RandomHorizontalFlip(),
                    T.ToTensor(),
                    T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
                ])
            else:
                self.transforms = T.Compose([
                    T.Resize(size=(288, 144)),
                    T.ToTensor(),
                    T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
                ])

    def __getitem__(self, index):
        '''
        一次返回一张图片的数据
        '''
        img_path = self.train_data[index][0]
        i = self.train_data[index][1]
        id = self.train_data[index][2]
        cam = self.train_data[index][3]
        label = np.asarray(self.train_attr[id])
        data = Image.open(img_path)
        data = self.transforms(data)
        name = self.train_data[index][4]
        return data, i, label, id, cam, name

    def __len__(self):
        return len(self.train_data)

    def num_label(self):
        return self.num_labels

    def num_id(self):
        return self.num_ids

    def labels(self):
        return self.label