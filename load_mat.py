import scipy.io
import numpy as np
import json
mat = scipy.io.loadmat('market_attribute.mat')['market_attribute'][0][0]
test, train = mat
# print(len(test[0][0]))
# label = test.dtype
label_test =[]
label_train =[]
for i in ['test', 'train']:
    for lab, index in globals()[i].dtype.fields.items():
        globals()[f'label_{i}'].append(lab)
    globals()[f'label_{i}'] = globals()[f'label_{i}'][:-1]
id_train = []
id_test = []
data = dict()
for i in ['test', 'train']:
    for id_person in globals()[i][0][0][27][0]:
        globals()[f'id_{i}'].append(id_person[0])
for i in ['test', 'train']:
    data[i] = dict()
    for id_ in globals()[f'id_{i}']:
        data[i][id_] = dict()
for i in ['test', 'train']:
    for index, label in enumerate(globals()[f'label_{i}']):
        globals()[label] = globals()[i][0][0][index][0]
        if label != 'age':
            for count, id_ in enumerate(globals()[f'id_{i}']):
                if globals()[label][count] -1 == 0:
                    data[i][id_][label] = None
                else:
                    data[i][id_][label] = True
                # data[i][id_].append(globals()[label][count] -1)
        else:
            for count, id_ in enumerate(globals()[f'id_{i}']):
                if globals()[label][count]  == 0:
                    data[i][id_][label] = 'young'
                elif globals()[label][count]  == 1: 
                    data[i][id_][label] = 'teenager'
                elif globals()[label][count]  == 2: 
                    data[i][id_][label] = 'adult'
                else:
                    data[i][id_][label] = 'old'
data_final = dict()
data_final.update(data['test'])
data_final.update(data['train'])
with open('./doc/dataset_attrbute.json', 'w') as file:
    json.dump(data_final, file, indent = 4)