import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

f = open('authornames.txt', 'r')

nodes = []
listofLines = []

for line in f:
	line.rstrip()
	_line = line.split(",")
	temp = []
	for name in _line:
		nodes.append(name.strip('\n').lstrip())
		temp.append(name.strip('\n').lstrip())
	listofLines.append(temp)

f.close()
G.add_nodes_from(nodes)

#there are 566 authors and 178 papers
#how should I add edges to this graph? should I make an adjacency matrix first? 

for i in range(178):
	l = len(listofLines[i]) 
	for j in range(l):
		for k in range(j + 1, l):
			G.add_edge(listofLines[i][j], listofLines[i][k])

plt.figure(figsize=(8,8))

# nx.draw_networkx_edges(G, pos, alpha=0.4)
# nx.draw_networkx_nodes(G, pos, node_size=80, cmap=plt.cm.Reds_r)

plt.xlim(-0.05,1.05)
plt.ylim(-0.05,1.05)
plt.axis('off')

nx.draw(G)
plt.savefig('_graph.png')
plt.show()