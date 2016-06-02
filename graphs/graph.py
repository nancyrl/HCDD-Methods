import networkx as nx
from networkx.readwrite import json_graph
import numpy as np
import csv
import sys
import matplotlib.pyplot as plt
import json
import pickle

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
	# lastnames = set()
	# duplicates = set()

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
				author = row[i].rstrip().lstrip()
				authors.add(author)
				# last_name = author.split(" ")
				# last_name = ' '.join(last_name[1:])
				# if last_name in lastnames:
				# 	duplicates.add(last_name)
				# else:
				# 	lastnames.add(last_name)
			
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
	# print('Unique number of last names: ' + str(len(lastnames)))
	# print(duplicates)
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

def read_from_csv(filename): 

	author_matrix = []
	author_nodes_set = set()

	#filtering out the nodes from csv
	with open(filename, 'r') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		for row in reader:
			#skip the first row
			if 'First Author' in row:
				continue
			line = []
			for i in range(len(row)):
				if row[i] != '':
					line.append(row[i])
					author_nodes_set.add(row[i])
			author_matrix.append(line)

	return {'author_matrix': author_matrix, 'author_nodes': author_nodes_set}

def generate_author_to_int_dictionary(filename):

	retdict = read_from_csv(filename)
	author_nodes = retdict['author_nodes']
	author_matrix = retdict['author_matrix']

	#assigning each author an integer representation
	author_to_int = dict()
	i = 0
	for item in sorted(author_nodes):
		author_to_int[item] = i
		i += 1

	#saving the author to int dictionary
	pickle.dump(author_to_int, open("author_int_dict.p", "wb"))
	pickle.dump(author_matrix, open("author_matrix.p", "wb"))

def generate_adj_matrix():

	author_to_int = pickle.load(open("author_int_dict.p", "rb"))
	author_matrix = pickle.load(open("author_matrix.p", "rb"))

	#initializing adjacency matrix
	size = len(author_to_int)
	M = [[0 for i in range(size)] for j in range(size)]

	#adding edges from each author
	for paper in range(len(author_matrix)):
		num_authors = len(author_matrix[paper])
		for j in range(num_authors):
			a1 = author_matrix[paper][j]
			for k in range(j + 1, num_authors):
				a2 = author_matrix[paper][k]
				M[author_to_int[a1]][author_to_int[a2]] = 1
				M[author_to_int[a2]][author_to_int[a1]] = 1

	pickle.dump(M, open("adjacency_matrix.p", "wb"))

	#save graph and dict info into a readable text file for debugging
	with open('adjacency_matrix.txt', 'w') as f: 
		f.write("Authors to Integers Dictionary \n")
		#listing authors by their values
		for item in sorted(author_to_int, key=author_to_int.get):
			f.write(str(item) + " : " + str(author_to_int[item]) + "\n")
		f.write("\n\n\nPure python matrix: \n\n")
		for row in M: 
			f.write(str(row).strip("]").strip("[") + "\n")

def generate_networkX_graph_int():

	global G
	G = nx.Graph()
	author_to_int = pickle.load(open("author_int_dict.p", "rb"))
	matrix = pickle.load(open("adjacency_matrix.p", "rb"))

	#adding each int to the graph G
	for key in author_to_int: 
		G.add_node(author_to_int[key])

	s = len(matrix)
	for i in range(s):
		for j in range(s):
			if matrix[i][j] == 1:
				G.add_edge(i, j)

	write_json('int')

def generate_networkX_graph_string():

	global G
	G = nx.Graph()
	author_to_int = pickle.load(open("author_int_dict.p", "rb"))
	author_matrix = pickle.load(open("author_matrix.p", "rb"))

	#adding each author's name to the graph G
	for key in author_to_int: 
		G.add_node(key)

	for row in range(len(author_matrix)):
		num_authors = len(author_matrix[row])
		for j in range(num_authors):
			a1 = author_matrix[row][j]
			for k in range(j + 1, num_authors):
				a2 = author_matrix[row][k]
				G.add_edge(a1, a2)

	write_json('string')

def write_json(type):

	if type == 'int':
		with open('data_int.json', 'w') as outfile1:
			outfile1.write(json.dumps(json_graph.node_link_data(G)))
		print('Dumped into file <data_int.json>.')

	elif type == 'string':
		with open('data_string.json', 'w') as outfile1:
			outfile1.write(json.dumps(json_graph.node_link_data(G)))
		print('Dumped into file <data_string.json>.')

def nx_draw_graph():

	plt.figure(figsize=(8,8))
	plt.xlim(-0.05,1.05)
	plt.ylim(-0.05,1.05)
	plt.axis('off')
	nx.draw(G)
	plt.savefig('graph_new.png')
	plt.show()

def main():

	#input: python graphdraft.py <input.txt> <csvfile>
	text_file = sys.argv[1]
	csv_file = sys.argv[2]

	convert_text_to_csv(text_file, csv_file)
	simple_stats(csv_file)

	print("Now generating json graph information...")

	#optional; if dict and matrix pickle files already exist, do not execute the below lines
	generate_author_to_int_dictionary(csv_file)
	generate_adj_matrix()

	generate_networkX_graph_string()

	return "Finished"
                
if __name__ == "__main__":
    main()