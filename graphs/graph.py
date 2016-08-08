import preprocess
import metrics
import networkx as nx
from networkx.readwrite import json_graph
import csv
import sys
import pickle
import matplotlib.pyplot as plt
import json


def read_from_csv(filename): 
	author_matrix, author_nodes_set = [], set()
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
	author_to_int, i = dict(), 0
	sorted_authors = sorted(author_nodes)
	for item in sorted_authors:
		author_to_int[item] = i
		i += 1
	pickle.dump(author_to_int, open("author_int_dict.p", "wb"))
	pickle.dump(author_matrix, open("author_matrix.p", "wb"))

def generate_adj_matrix():
	author_to_int = pickle.load(open("author_int_dict.p", "rb"))
	author_matrix = pickle.load(open("author_matrix.p", "rb"))

	size = len(author_to_int)
	M = [[0 for i in range(size)] for j in range(size)]
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
		for item in sorted(author_to_int, key=author_to_int.get):
			f.write(str(item) + " : " + str(author_to_int[item]) + "\n")
		f.write("\n\n\nPure python matrix: \n\n")
		for row in M: 
			f.write(str(row).strip("]").strip("[") + "\n")

def generate_networkX_graph_int():
	G = nx.Graph()
	author_to_int = pickle.load(open("author_int_dict.p", "rb"))
	matrix = pickle.load(open("adjacency_matrix.p", "rb"))

	for key in author_to_int: 
		G.add_node(author_to_int[key])

	s = len(matrix)
	for i in range(s):
		for j in range(s):
			if matrix[i][j] == 1:
				G.add_edge(i, j)
	return G

def generate_networkX_graph_string(weighted=False):
	G = nx.Graph()
	author_to_int = pickle.load(open("author_int_dict.p", "rb"))
	author_matrix = pickle.load(open("author_matrix.p", "rb"))

	if not weighted: 
		for key in author_to_int: 
			G.add_node(key)
		num_papers = len(author_matrix)
		for row in range(num_papers):
			num_authors = len(author_matrix[row])
			for j in range(num_authors):
				a1 = author_matrix[row][j]
				for k in range(j + 1, num_authors):
					a2 = author_matrix[row][k]
					G.add_edge(a1, a2)
	else:
		#construct dictionary from papers_per_author.csv
		papers_per_author_dict = dict()
		with open('papers_per_author.csv', 'r') as csvf:
			reader = csv.reader(csvf, delimiter=',')
			for row in reader:
				if row[0] == 'Author':
					continue
				papers_per_author_dict[row[0]] = int(row[1])
		for key in author_to_int: 
			node_value = papers_per_author_dict[key]
			G.add_node(key, value=node_value)
		seen_edge_pairs = dict()
		num_papers = len(author_matrix)
		for row in range(num_papers):
			num_authors = len(author_matrix[row])
			for j in range(num_authors):
				a1 = author_matrix[row][j]
				for k in range(j + 1, num_authors):
					a2 = author_matrix[row][k]
					author_pair = a1 + ', ' + a2
					if author_pair not in seen_edge_pairs:
						G.add_edge(a1, a2, weight=1)
						seen_edge_pairs[author_pair] = 1
					else: 
						G[a1][a2]['weight'] += 1
						seen_edge_pairs[author_pair] += 1

		with open('pairs_publications.txt', 'w') as f: 
			f.write('Pairs of publishing authors and their number of publications: \n')
			seen_list = sorted(seen_edge_pairs, key=seen_edge_pairs.get)
			for key in seen_list:
				f.write(key + ' ' + str(seen_edge_pairs[key]) + '\n')
		print('Saved author link weights into pairs_publications.txt.')
	return G

def write_json(G, type, weighted=False):
	if not weighted: 
		if type == 'int':
			with open('data_int.json', 'w') as outfile1:
				outfile1.write(json.dumps(json_graph.node_link_data(G)))
			print('Dumped into file <data_int.json>.')

		elif type == 'string':
			with open('data_string.json', 'w') as outfile1:
				outfile1.write(json.dumps(json_graph.node_link_data(G)))
			print('Dumped into file <data_string.json>.')
	else:
		if type == 'int':
			with open('data_int_weighted.json', 'w') as outfile1:
				outfile1.write(json.dumps(json_graph.node_link_data(G)))
			print('Dumped into file <data_int_weighted.json>.')

		elif type == 'string':
			with open('data_string_weighted.json', 'w') as outfile1:
				outfile1.write(json.dumps(json_graph.node_link_data(G)))
			print('Dumped into file <data_string_weighted.json>.')

def nx_draw_graph():
	plt.figure(figsize=(8,8))
	plt.xlim(-0.05,1.05)
	plt.ylim(-0.05,1.05)
	plt.axis('off')
	nx.draw(G)
	plt.savefig('graph_new.png')
	plt.show()

def main():
	try: 
		text_file, csv_file = sys.argv[1], sys.argv[2]
		preprocess.convert_text_to_csv(text_file, csv_file)
		preprocess.simple_stats(csv_file)
		print("Now generating json graph information...")
		generate_author_to_int_dictionary(csv_file)
		generate_adj_matrix()
		G = generate_networkX_graph_string()
		write_json(G, 'string')
		G_s = generate_networkX_graph_string(True)
		write_json(G_s, 'string', weighted=True)
		print("Now calculating metrics...")
		metrics.calculate_metrics()
	except IndexError as err:
		print('Please type python graph.py <input.txt> <output.csv>.')
		sys.exit()


                
if __name__ == "__main__":
    main()
