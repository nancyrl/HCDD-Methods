import networkx as nx
import csv
import sys
import matplotlib.pyplot as plt
from networkx.readwrite import json_graph
import json

G = nx.Graph()

def generate_graph(filename):

	author_matrix = []

	with open(filename, 'r') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		for row in reader:
			if 'First Author' in row:
				continue
			line = []
			for i in range(len(row)):
				if row[i] != '':
					G.add_node(row[i])
					line.append(row[i])
			author_matrix.append(line)

	for paper in range(len(author_matrix)):
		num_authors = len(author_matrix[paper]) 
		for j in range(num_authors):
			for k in range(j + 1, num_authors):
				G.add_edge(author_matrix[paper][j], author_matrix[paper][k])

	print (author_matrix)

def draw_graph():

	# plt.figure(figsize=(8,8))

	# plt.xlim(-0.05,1.05)
	# plt.ylim(-0.05,1.05)
	# plt.axis('off')

	# nx.draw(G)
	# plt.savefig('_graph.png')
	# plt.show()

	with open('networkdata1.json', 'w') as outfile1:
		outfile1.write(json.dumps(json_graph.node_link_data(G)))


def main():

	csv_file = sys.argv[1]
	generate_graph(csv_file)
	draw_graph()

	return "Finished"
                
if __name__ == "__main__":
    main()