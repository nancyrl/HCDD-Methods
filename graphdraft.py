import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
# G.position = {}

f = open('authors.txt', 'r')

nodes = []
edges = []

for line in f:
	_line = line.split(",")
	paper = []
	for _ in _line:
		author = _.strip('\n').strip('\t').lstrip().rstrip()
		G.add_node(author)
		paper.append(author)

	edges.append(paper)
f.close()

#there are 276 authors and 87 papers

for paper in range(83):
	l = len(edges[paper]) 
	for j in range(l):
		for k in range(j + 1, l):
			G.add_edge(edges[paper][j], edges[paper][k])

plt.figure(figsize=(8,8))

# nx.draw_networkx_edges(G, pos, alpha=0.4)
# nx.draw_networkx_nodes(G, pos, node_size=80, cmap=plt.cm.Reds_r)

plt.xlim(-0.05,1.05)
plt.ylim(-0.05,1.05)
plt.axis('off')

nx.draw(G)
plt.savefig('_graph.png')
plt.show()