import json
import os
def import_attribute(datapath):
	for mode in ['train', 'val']:
		globals()[mode] = dict()
		print(os.path.join(datapath, mode, 'attribute'))
		for root, dirs, files in os.walk(os.path.join(datapath, mode, 'attribute')):
			for file in files:
				if file.endswith('.json'):
					id_ = file[:4]
					with open(os.path.join(root, file),'r') as f:
						attribute = json.load(f)
					keys = list(attribute.keys())
					arr = []
					for i, key in enumerate(keys):
						arr.insert(i,int(attribute[key]))
					globals()[mode][id_] = arr
	return train, val, keys
def import_MarketDuke_nodistractors(dataset_dir):   
    if not os.path.exists(dataset_dir):
        print('Please Download '+dataset_name+ ' Dataset')    
    data_group = ['train','val']
    for group in data_group:
        if group == 'train':
            name_dir = os.path.join(dataset_dir , 'train')
        elif group == 'val':
            name_dir = os.path.join(dataset_dir, 'val')
        file_list=sorted(os.listdir(name_dir))
        globals()[group]={}
        globals()[group]['data']=[]
        globals()[group]['ids'] = []
        for root, dirs, files in os.walk(os.path.join(dataset_dir, group, 'images')):
            for file in files:
                if file.endswith('.jpg'):
                    id = file[:4]
                    cam = 1
                    images = os.path.join(root, file)
                    if id not in globals()[group]['ids']:
                        globals()[group]['ids'].append(id)
                    globals()[group]['data'].append([images,globals()[group]['ids'].index(id),id,cam,file.split('.')[0]])
    return train, val
   