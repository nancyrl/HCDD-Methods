import csv

""" This is a snippet of code I wrote to regenerate the authors.txt file after deleting it.
"""
# f = open('finalauthors.txt', 'w+')
# with open('separated-authors.csv', 'r') as csvfile:
# 	reader = csv.reader(csvfile, delimiter=',')
# 	for row in reader:
# 		line = row[0]
# 		for i in range(1, 11):
# 			line = line + ', ' + row[i]
# 		print(line)
# 		f.write(line + '\n')
# f.close()

""" Code to parse dataset, pull out relevant data (place of publication of first authors and other authors,
 and place into text file for easier processing.
"""

# f = open('countrydraft.txt', 'w')

# with open('dataset.csv', 'r') as csvfile:
# 	reader = csv.reader(csvfile, delimiter=',')
# 	for row in reader:
# 		f.write(row[10] + ' | ' + row[12] + '\n')
# 		print(row[10] + ' ==== ' + row[12])

# f.close()


"""reads the file produced by above to create the relevant csv"""

# f = open('countrydraft.txt', 'r')

# firstCountries = dict()
# otherCountries = dict()
# check = set()

# for line in f: 
# 	arrLine = line.split(' | ')
# 	firstC = arrLine[0].split(',')
# 	secC = arrLine[1].split(',')

# 	for _ in firstC:
# 		_ = _.lstrip().rstrip().strip('\n')
# 		if _ in firstCountries:
# 			firstCountries[_] += 1
# 		else: 
# 			firstCountries[_] = 1
# 		check.add(_)

# 	for _ in secC:
# 		_ = _.lstrip().rstrip().strip('\n')
# 		if _ in otherCountries:
# 			otherCountries[_] += 1
# 		else: 
# 			otherCountries[_] = 1

# print(firstCountries)
# print(otherCountries)

# f.close()

# with open('countryinfo.csv', 'w', newline='') as csvfile:
# 	writer = csv.writer(csvfile)
# 	writer.writerow(('Country', 'Number of First Authors', 'Number of Other Authors'))
# 	for key in firstCountries:
# 		if key in otherCountries:
# 			writer.writerow((key, firstCountries[key], otherCountries[key]))
# 		elif key not in otherCountries:
# 			writer.writerow((key, firstCountries[key], '0'))
# 		check.add(key)
# 	for key in otherCountries:
# 		if key not in check: 
# 			if key in firstCountries:
# 				writer.writerow((key, firstCountries[key], otherCountries[key]))
# 			elif key not in firstCountries:
# 				writer.writerow((key, '0', otherCountries[key]))

""" Code to parse dataset, pull out place of work done,
 and place into text file for easier processing.
"""

# f = open('countrydraft2.txt', 'w')

# with open('dataset.csv', 'r') as csvfile:
# 	reader = csv.reader(csvfile, delimiter=',')
# 	for row in reader:
# 		f.write(row[13] +'\n')
# 		print(row[13])

# f.close()

""" Code to analyze the countrydraft2 file"""

countries = dict()

f = open('countrydraft2.txt', 'r')
for line in f: 
	arrLine = line.split(',')
	for _ in arrLine:
		_ = _.lstrip().rstrip().strip('\n')
		if _ in countries:
			countries[_] += 1
		else: 
			countries[_] = 1
f.close()

with open('countrywork.csv', 'w', newline='') as csvfile:
	writer = csv.writer(csvfile)
	writer.writerow(('Country', 'Number of Mentions as Place of Work'))
	for key in countries:
		writer.writerow((key, str(countries[key])))