import cv2, json
from PIL import Image
import glob, os
import threading
import sys
import torch
import psutil
def destroyAllwindow():
	for proc in psutil.process_iter():
	    if proc.name() == "display":
	        proc.kill()
start = int(input('Stating wwith id_person: '))
path_img = 'D:/WORKIT/Person-Attribute-Recognition-MarketDuke/dataset/id'
saveattribute = 'D:/WORKIT/Person-Attribute-Recognition-MarketDuke/dataset/attribute'
with open('./doc/label.txt', 'r') as f:
	attribute = [i.replace('\n', '') for i in f.readlines() if i != '']
	print(attribute)
'''Arguments
======================================================================='''
old_id = ''
color = {'w':'white', 'b':'black', 'y':'yellow', 'bl':'blue', 'g':'green', 'r':'red', 'or':'orange', 'p':'pink', 'gr':'gray', 'br':'brown', 'pu':'purple'}
key_color = list(color.keys())
#=======================================================================
for root, dirs, files in os.walk(path_img):
	for file in files:
		if file.endswith('.jpg'):
			id_person = root[-4:]
			if id_person!=old_id and int(id_person)>=start:
				dict_att = dict()
				sex = ''
				ages = ''
				hair = ''
				hat = ''
				scaft = ''
				bag = ''
				glasses = ''
				cloth_up = ''
				cloth_up_color = ''
				cloth_below = ''
				cloth_below_color = ''
				shoe = ''
				shoe_color = ''
				# print(os.path.join(root, file))
				# img = Image.open(os.path.join(root, file))
				# # img = cv2.imread(os.path.join(root, file))
				# w, h= img.size
				# img = img.resize((350, int(350*h/w)))
				# img.show()
				print(id_person.center(50, '='))
				old_id = id_person
				while sex not in [0, 1]:
					sex = int(input('Boy = 0/ Girl = 1'.ljust(50, ' ')))
				dict_att['sex'] = sex
				while ages not in ['0' , '1', '2']:
					ages = input('KID=0/teenage=1/adult=2'.ljust(50, ' '))
					if int(ages) == 0:
						globals()[attribute[0]] = 1
						globals()[attribute[1]] = 0
						globals()[attribute[2]] = 0
					elif int(ages)==1:
						globals()[attribute[0]] = 0
						globals()[attribute[1]] = 1
						globals()[attribute[2]] = 0
					elif int(ages)== 2:
						globals()[attribute[0]] = 0
						globals()[attribute[1]] = 0
						globals()[attribute[2]] = 1
				dict_att['kid'], dict_att['teenage'], dict_att['adult'] = globals()[attribute[0]], globals()[attribute[1]], globals()[attribute[2]]
				while hair not in [0, 1]:
					hair = int(input('Short hair= 0/ Long hair= 1'.ljust(50, ' ')))
				dict_att['hair'] = hair
				while hat not in [0, 1]:
					hat = int(input('Have hat= 1/ No hat = 0'.ljust(50, ' ')))
				dict_att['hat'] = hat
				while scaft not in [0, 1]:
					scaft = int(input('Have scaft = 1/No scaft = 0'.ljust(50, ' ')))
				dict_att['scaft'] = scaft
				while glasses not in [0, 1]:
					glasses = int(input('Have glasses = 1/No glasses = 0'.ljust(50, ' ')))
				dict_att['glasses'] = glasses
				while bag not in [0, 1]:
					bag = int(input('Have bag = 1/No bag = 0'.ljust(50, ' ')))
				dict_att['glasses'] = glasses
				#Cloth up ==========================================================
				while cloth_up not in [0, 1]:
					cloth_up = int(input('Have cloth_up = 1/No cloth_up = 0'.ljust(50, ' ')))
				dict_att['cloth_up'] = cloth_up
				if cloth_up == 1:
					while cloth_up_color not in ['w', 'b', 'y', 'bl', 'g', 'r', 'or', 'p', 'gr', 'br', 'pu', '0']:
						cloth_up_color = input('Color: w-white\nb-black\ny-yellow\nbl-blue\ng-green\nr-red\nor-orange\np-pink\ngr-gray\nbr-brown\npu-purple\n').lower()
					if cloth_up_color == '0':
						for k in key_color:
							dict_att['cloth_up_'+color[k]] = 0
					else:
						dict_att['cloth_up_'+color[cloth_up_color]] = 1
						non_color = [keys for keys in key_color if keys != cloth_up_color]
						for k in non_color:
							dict_att['cloth_up_'+color[k]] = 0
				else:
					for k in key_color:
						dict_att['cloth_up_'+color[k]] = 0
				#Cloth down ==========================================================
				while cloth_below not in [0, 1]:
					cloth_below = int(input('Have cloth_below = 1/No cloth_below = 0'.ljust(50, ' ')))
				dict_att['cloth_below'] = cloth_below
				if cloth_below == 1:
					while cloth_below_color not in ['w', 'b', 'y', 'bl', 'g', 'r', 'or', 'p', 'gr', 'br', 'pu', '0']:
						cloth_below_color = input('Color: w-white\nb-black\ny-yellow\nbl-blue\ng-green\nr-red\nor-orange\np-pink\ngr-gray\nbr-brown\npu-purple\n').lower()
					if cloth_below_color == '0':
						for k in key_color:
							dict_att['cloth_below_'+color[k]] = 0
					else:	
						dict_att['cloth_below_'+color[cloth_below_color]] = 1
						non_color = [keys for keys in key_color if keys != cloth_below_color]
						for k in non_color:
							dict_att['cloth_below_'+color[k]] = 0
				else:
					for k in key_color:
						dict_att['cloth_below_'+color[k]] = 0
				#Shoe ==========================================================
				while shoe not in [0, 1]:
					shoe = int(input('Have shoe = 1/No shoe = 0'.ljust(50, ' ')))
				dict_att['shoe'] = shoe
				if shoe == 1:
					while shoe_color not in ['w', 'b', 'y', 'bl', 'g', 'r', 'or', 'p', 'gr', 'br', 'pu', '0']:
						shoe_color = input('Color: w-white\nb-black\ny-yellow\nbl-blue\ng-green\nr-red\nor-orange\np-pink\ngr-gray\nbr-brown\npu-purple\n').lower()
					if shoe_color == '0':
						for k in key_color:
							dict_att['shoe_'+color[k]] = 0
					else:
						dict_att['shoe_'+color[shoe_color]] = 1
						non_color = [keys for keys in key_color if keys != shoe_color]
						for k in non_color:
							dict_att['shoe_'+color[k]] = 0
				else:
					for k in key_color:
						dict_att['shoe_'+color[k]] = 0
				name_file = id_person + '.json'
				print(dict_att)
				with open(os.path.join(saveattribute, name_file), 'w') as jsonfile:
					jsonfile.write(json.dumps(dict_att, indent=4))