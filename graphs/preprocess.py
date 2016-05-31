"""Some preprocessing for the author dataset. HCD+D Methods."""

import csv
import sys


def count_authors_and_papers(filename):
	
	num_papers = 0
	linelengths = []
	with open(filename, 'r') as f:
		for line in f:
			arrLine = line.split(",")
			count = 0
			for name in arrLine:
				count += 1
			linelengths.append(count)
			num_papers += 1

	m = max(linelengths)
	return [m, num_papers]


def convert_text_to_csv(filename, outfile):

	retval = count_authors_and_papers(filename)
	max_authors = retval[0]
	num_papers = retval[1]
	all_authors = [[] for x in range(max_authors)] 

	with open(filename, 'r') as f:
		for line in f:
			arrLine = line.split(",")
			position = 0

			for name in arrLine:
				name = name.strip('\n').strip('\t').lstrip().rstrip()
				all_authors[position].append(name)
				position += 1

			while position < max_authors:
				all_authors[position].append('')
				position += 1
	
	return write_csv(all_authors, outfile, max_authors, num_papers)


def write_csv(all_authors, csvfilename, max_authors, num_papers):

	first_row = ['First Author']
	for i in range(2, max_authors + 1):
		first_row.append(str(i))

	with open(csvfilename, 'wt', newline='') as csvf:
		writer = csv.writer(csvf)
		writer.writerow(first_row)
		for j in range(num_papers):
			row = []
			for i in range(max_authors): 
				row.append(all_authors[i][j])
			writer.writerow(row)
	return

def simple_stats(filename):

	authors = set()
	linelengths = []
	num_papers = 0

	with open(filename, 'r') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		for row in reader:
			if row[0] == 'First Author':
				continue
			author_count = 0
			for i in range(len(row)):
				author_count += 1
				if row[i] == '':
					continue
				authors.add(row[i].rstrip().lstrip())
			
			linelengths.append(author_count)
			num_papers += 1
	m = max(linelengths)

	with open('simplestats.out', 'w') as f: 
		f.write('Max number of authors writing a single paper: ' + str(m) + '\n')
		f.write('Total unique number of authors: ' + str(len(authors)) + '\n')
		f.write('Total number of papers: ' + str(num_papers) + '\n')

	print(authors)
	print('Max number of authors writing a single paper: ' + str(m))
	print('Unique number of authors: ' + str(len(authors)))
	print('Number of papers: ' + str(num_papers))
	print('Done! This info has been saved to <simplestats.out>.')


#code to regenerate the authors.txt file after deleting it.
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

def main():
	""" On the command line, expected input is python preprocessing.py <inputtextfile.txt> <pathtooutput.csv> """

	in_text_file = sys.argv[1]
	out_csv_file = sys.argv[2]

	convert_text_to_csv(in_text_file, out_csv_file)
	simple_stats(out_csv_file)

	return "Finished!"
                
if __name__ == "__main__":
    main()