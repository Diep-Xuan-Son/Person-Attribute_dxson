import xlrd
import json
loc = ("H:\\Attribute_predict\\person_attribute\\13_04_2022.xlsx")
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
# For row 0 and column 0
label = sheet.row_values(0)[1:]
result = dict()
for i in range(1, sheet.nrows):
	data = sheet.row_values(i)
	ids = data[0]
	result[ids] = dict()
	for inter, i in enumerate(data[1:]):
		if i == 1:
			result[ids][label[inter]] = 1
		else:
			result[ids][label[inter]] = 0
with open("13_04_2022.json", "w") as f:
	json.dump(result,f, indent = 4)