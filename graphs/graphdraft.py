import networkx as nx
from networkx.readwrite import json_graph
import numpy as np
import csv
import sys
import matplotlib.pyplot as plt
import json
import pickle

G = nx.Graph()

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
	pickle.dump(author_to_int, open("a_int.p", "wb"))
	pickle.dump(author_matrix, open("a_matrix.p", "wb"))

def generate_matrix():

	author_to_int = pickle.load(open("a_int.p", "rb"))
	author_matrix = pickle.load(open("a_matrix.p", "rb"))

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
	# np.set_printoptions(precision=0)
	# np.set_printoptions(threshold=np.nan)
	npmatrix = nx.to_numpy_matrix(G)
	pickle.dump(M, open("adjacency_matrix.p", "wb"))

	#save graph info, dict info into a text file
	with open('adjmatrix.txt', 'w') as f: 
		f.write("Authors to Integers Dictionary \n")
		#listing authors by their values
		for item in sorted(author_to_int, key=author_to_int.get):
			f.write(str(item) + " : " + str(author_to_int[item]) + "\n")
		f.write("\n\n\nPure python matrix: \n\n")
		for row in M: 
			f.write(str(row).strip("]").strip("[") + "\n")

def generate_networkX_graph():
	author_to_int = pickle.load(open("a_int.p", "rb"))
	matrix = pickle.load(open("adjacency_matrix.p", "rb"))

	#adding each int to the graph G
	for key in author_to_int: 
		G.add_node(author_to_int[key])

	for i in range(len(matrix)):
		for j in range (len(matrix)):
			if matrix[i][j] == 1:
				G.add_edge(i, j)

	make_graph('node link')

def make_graph(type):

	plt.figure(figsize=(8,8))

	plt.xlim(-0.05,1.05)
	plt.ylim(-0.05,1.05)
	plt.axis('off')

	if type == 'node link':
		with open('data1.json', 'w') as outfile1:
			outfile1.write(json.dumps(json_graph.node_link_data(G)))
		print('Dumped into node link graph <data1.json>.')

	nx.draw(G)
	plt.savefig('graph_new.png')
	plt.show()


def main():

	#input: python graphdraft.py <path to csvfile of authors>

	if len(sys.argv) == 2:
		csv_file = sys.argv[1]
		generate_author_to_int_dictionary(csv_file)

	generate_matrix()
	generate_networkX_graph()

	return "Finished"
                
if __name__ == "__main__":
    main()