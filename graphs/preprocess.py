import csv

def count_authors_and_papers(filename):
	num_papers, line_len = 0, []
	with open(filename, 'r') as f:
		for line in f:
			arrLine = line.split(",")
			count = 0
			for name in arrLine:
				count += 1
			line_len.append(count)
			num_papers += 1
	return [max(line_len), num_papers]

def convert_text_to_csv(filename, outfile):
	retval = count_authors_and_papers(filename)
	max_authors, num_papers = retval[0], retval[1]
	all_authors = [[] for x in range(max_authors)] 
	with open(filename, 'r') as f:
		for line in f:
			arrLine = line.split(",")
			pos = 0
			for name in arrLine:
				name = name.strip('\n').strip('\t').lstrip().rstrip()
				all_authors[pos].append(name)
				pos += 1
			while pos < max_authors:
				all_authors[pos].append('')
				pos += 1
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

def simple_stats(filename):
	authors, linelengths, num_papers = set(), [], 0
	stats = dict()
	# lastnames = set()
	# duplicates = set()
	with open(filename, 'r') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		for row in reader:
			if row[0] == 'First Author':
				continue
			author_count = 0
			for i in range(len(row)):
				if row[i] == '':
					continue
				author_count += 1
				author = row[i].rstrip().lstrip()
				authors.add(author)
				# last_name = author.split(" ")
				# last_name = ' '.join(last_name[1:])
				# if last_name in lastnames:
				# 	duplicates.add(last_name)
				# else:
				# 	lastnames.add(last_name)
				if author in stats:
					stats[author] += 1
				else: 
					stats[author] = 1 				
				linelengths.append(author_count)
			num_papers += 1
	m = max(linelengths)

	with open('simplestats.out', 'w') as f: 
		f.write('Max number of authors writing a single paper: ' + str(m) + '\n')
		f.write('Total unique number of authors: ' + str(len(authors)) + '\n')
		f.write('Total number of papers: ' + str(num_papers) + '\n')
	with open('papers_per_author.csv', 'wt', newline='') as csvf:
		writer = csv.writer(csvf)
		writer.writerow(['Author', 'Number of Papers'])
		for key in sorted(stats, key=stats.get):
			writer.writerow([key, str(stats[key])])

	print(authors)
	print('Max number of authors writing a single paper: ' + str(m))
	print('Unique number of authors: ' + str(len(authors)))
	print('Number of papers: ' + str(num_papers))
	# print('Unique number of last names: ' + str(len(lastnames)))
	# print(duplicates)
	print('Info has been saved to <simplestats.out>.')
	print('Number of papers per author has been saved to <papers_per_author.csv>.')