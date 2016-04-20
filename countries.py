import csv

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

# f = open('countrydraft.txt', 'w')

# with open('dataset.csv', 'r') as csvfile:
# 	reader = csv.reader(csvfile, delimiter=',')
# 	for row in reader:
# 		f.write(row[10] + ' | ' + row[12] + '\n')
# 		print(row[10] + ' ==== ' + row[12])

# f.close()

dictionary crap goes here

f = open('countrydraft.txt', 'r')

firstCountries = set()
otherCountries = set()

for line in f: 
	arrLine = line.split(' | ')
	firstC = arrLine[1].split(',')
	for _ in firstC:
		firstCount
