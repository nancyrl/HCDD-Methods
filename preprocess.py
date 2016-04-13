"""Some preprocessing for the author dataset. HCD+D Methods."""

import csv
import sys

def simplestats(filename):

	f = open(filename, 'r')
	authors = []
	linelengths = []
	global all_authors, num_papers
	all_authors = [[] for x in range(11)] 
	num_papers = 0

	for line in f:
		line.rstrip()
		arrLine = line.split(",")
		count = 0
		position = 0

		for name in arrLine:
			count += 1
			name = name.strip('\n').strip('\t').lstrip()
			all_authors[position].append(name)
			position += 1
			if name not in authors:
				authors.append(name)

		while position < 11:
			all_authors[position].append(' ')
			position += 1

		linelengths.append(count)
		num_papers += 1

	f.close()
	m = max(linelengths)
	print(authors)
	print('Max number of authors writing a single paper is: ' + str(m))
	print('Unique number of authors is: ' + str(len(authors)))
	print('Number of papers is: ' + str(num_papers))
	return

def writecsv(filename):

	csvf = open(filename, 'wt', newline='')
	writer = csv.writer(csvf)
	writer.writerow(('First Author', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11'))
	for j in range(num_papers):
	    writer.writerow((all_authors[0][j], all_authors[1][j], all_authors[2][j], all_authors[3][j], all_authors[4][j], all_authors[5][j], all_authors[6][j], all_authors[7][j], all_authors[8][j], all_authors[9][j], all_authors[10][j]))
	csvf.close()
	return

""" On the command line, input: python preprocessing.py <yourtextfile.txt> <output.csv> """

simplestats(sys.argv[1])
writecsv(sys.argv[2])