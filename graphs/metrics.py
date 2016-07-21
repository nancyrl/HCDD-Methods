import graph
import pickle
import statistics
import copy
import math
import csv
import networkx as nx
import sys

def calc_mode(array):
    most = max(list(map(array.count, array)))
    return list(set(filter(lambda x: array.count(x) == most, array)))
    
def density_per_component(list_of_ints, matrix, author_to_int):
	inverse_author_dict = {v: k for k, v in author_to_int.items()}
	v = len(matrix)
	d_per_cc, d = dict(), 0
	for cc in list_of_ints:
		e = 0
		cc_size = len(cc)
		for i in cc: 
			for j in range(v): 
				if matrix[i][j] == 1:
					e += 1
		translated = [inverse_author_dict[int] for int in cc]
		print(str(cc))
		try: 
			d = (e) / (cc_size*(cc_size-1))
			print('Density: ' + str(d) + '\n')
		except ZeroDivisionError as err:
			if len(cc) == 1:
				d = 1
				print('Density: 1 \n')
			else:
				d = 0
				print("Uh oh. Something went wrong...")
		d_per_cc[str(translated)] = d 
	return d_per_cc
	# d = 0.017539133818203587

def betweenness_centrality():
	between = nx.betweenness_centrality(G)
	sorted_between = sorted(between, key=between.get)
	stats = [between[key] for key in sorted_between]
	average = statistics.mean(stats)
	median = statistics.median(stats)
	median_low = statistics.median_low(stats)
	median_high = statistics.median_high(stats)
	mode = calc_mode(stats)

	with open('betweenness_centrality.txt', 'w') as f: 
		for author in sorted_between:
			f.write(author + ": " + str(between[author]) + '\n')
		f.write('\nAverage: ' + str(average) + '\n')
		f.write('Median: ' + str(median) + '\n')
		f.write('Median low: ' + str(median_low) + '\n')
		f.write('Median high: ' + str(median_high) + '\n')
		f.write('Mode: ' + str(median_high) + '\n')	
	
	with open('betweenness_centrality.csv', 'wt', newline='') as csvf:
		writer = csv.writer(csvf)
		writer.writerow(['Author', 'Betweenness Centrality'])
		for author in sorted_between:
			writer.writerow([author, str(between[author])])

	print("Average betweenness is: " + str(average))
	# 6.894441787211672e-05			

def clustering_coefficient():
	coeff = nx.clustering(G)
	sorted_coeff = sorted(coeff, key=coeff.get)
	stats = [coeff[key] for key in sorted_coeff]
	average = statistics.mean(stats)
	median = statistics.median(stats)
	median_low = statistics.median_low(stats)
	median_high = statistics.median_high(stats)
	mode = calc_mode(stats)

	with open('clustering_coefficient.txt', 'w') as f: 
		for author in sorted_coeff:
			f.write(author + ": " + str(coeff[author]) + '\n')
		f.write('\nAverage: ' + str(average) + '\n')
		f.write('Median: ' + str(median) + '\n')
		f.write('Median low: ' + str(median_low) + '\n')
		f.write('Median high: ' + str(median_high) + '\n')
		f.write('Mode: ' + str(median_high) + '\n')	
	
	with open('clustering_coefficient.csv', 'wt', newline='') as csvf:
		writer = csv.writer(csvf)
		writer.writerow(['Author', 'Clustering Coefficient'])
		for author in sorted_coeff:
			writer.writerow([author, str(coeff[author])])
	
	print ("Average clustering is: " + " " + str(average))
	#clustering coefficient : 0.8099788585502871

def closeness_centrality():
	closeness = nx.closeness_centrality(G)
	sorted_closeness = sorted(closeness, key=closeness.get)
	stats = [closeness[key] for key in sorted_closeness]
	average = statistics.mean(stats)
	median = statistics.median(stats)
	median_low = statistics.median_low(stats)
	median_high = statistics.median_high(stats)
	mode = calc_mode(stats)

	with open('closeness_centrality.txt', 'w') as f: 
		for author in sorted_closeness:
			f.write(author + ": " + str(closeness[author]) + '\n')
		f.write('\nAverage: ' + str(average) + '\n')
		f.write('Median: ' + str(median) + '\n')
		f.write('Median low: ' + str(median_low) + '\n')
		f.write('Median high: ' + str(median_high) + '\n')
		f.write('Mode: ' + str(median_high) + '\n')	

	with open('closeness_centrality.csv', 'wt', newline='') as csvf:
		writer = csv.writer(csvf)
		writer.writerow(['Author', 'Closeness centrality'])
		for author in sorted_closeness:
			writer.writerow([author, str(closeness[author])])

	print ("Average closeness is: " + " " + str(average))
	# 0.02251066871887446
	
def diameter(matrix):
	v = len(matrix)
	d, inf = [], 100000
	dist = [[inf for x in range(v)] for y in range(v)]
	
	#constructing dist matrix
	for i in range(v):
		dist[i][i] = 0
		for j in range(v):
			if matrix[i][j] == 1:
				dist[i][j] = 1
	#floyd warshall algorithm
	for k in range(v):
		for i in range(v):
			for j in range(v):
				dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
	for i in range(v):
		for j in range(v):
			if i != j and dist[i][j] != inf:
				d.append(dist[i][j])
	diameter = max(d)
	print('Diameter of graph: ' + str(diameter) + '\n')

def cut_point(author_to_int): 
	adj_list = pickle.load(open("adj_list.p", "rb"))
	list_of_ints = pickle.load(open("list_of_ints.p", "rb"))
	final = set()
	for cc in list_of_ints:
		if len(cc) <= 4:
			continue
		cc = sorted(cc)
		print("Connected component: " + str(cc))
		cut_points = find_cut_points_in_cc(adj_list, cc)
		if not cut_points:
			print("There are no cut points.")
		else: 
			print("Cut points: " + str(cut_points))
			new_cut_points = filter_cut_points(adj_list, cut_points, cc)
			if not new_cut_points:
				print("All filtered out. \n")
			elif new_cut_points == cut_points:
				print("Nothing was filtered. \n")
			else: 
				print("Filtered cut points: " + str(new_cut_points) + "\n")
		final = final.union(new_cut_points)
	if final:
		inverse_author_dict = {v: k for k, v in author_to_int.items()}
		translated = [inverse_author_dict[int] for int in final]
		print("Cut points for all ccs: " + str(translated))
	else:
		print("No cut points.")

def find_cut_points_in_cc(graph, cc):
	v = len(graph)
	visited, prev = [False for _ in range(v)], [None for _ in range(v)]
	discover, low = [0 for _ in range(v)], [0 for _ in range(v)]
	cut_points = set()

	def cut_dfs(start):
		visited[start] = True
		nonlocal time
		time += 1
		low[start] = discover[start] = time
		for w in graph[start]:
			if not visited[w]:
				prev[w] = start
				cut_dfs(w)
				low[start] = min(low[start], low[w])
			elif w != prev[start]: 
				#then w is visited, and (start, w) must be a back edge
				low[start] = min(low[start], discover[w]) 

	for vertex in cc:
		if not visited[vertex]:
			time = 0
			cut_dfs(vertex)
		break #cc is connected so only one iteration is needed

	for vertex in cc:
		if prev[vertex] == None:
			if len(graph[vertex]) > 1:
				cut_points.add(vertex)
		else:
			for w in graph[vertex]:
				if low[w] >= discover[vertex]:
					cut_points.add(vertex)
	return cut_points

def filter_cut_points(graph, cut_points, cc):
	v = len(graph)
	filtered_cut_points = set()

	for cut in cut_points:
		new_graph = copy.deepcopy(graph)
		for edge in new_graph: 
			if cut in edge: 
				edge.remove(cut)
		metavisited, small_ccs = [False for _ in range(v)], []
		for vertex in cc:
			if vertex != cut and not metavisited[vertex]:
				ret = dfs(metavisited, vertex, new_graph)
				small_ccs.append(ret[0])
				metavisited = ret[1]
		if len(small_ccs) >= 2:
			filtered_cut_points.add(cut)
		print("Cut vertex: " + str(cut))
		print(str(small_ccs))
	return filtered_cut_points

def dfs(metavisited, start, graph):
	visited, stack = set(), [start]
	while stack:
		vertex = stack.pop()
		if vertex not in visited: 
			metavisited[vertex] = True
			visited.add(vertex)
			stack.extend(graph[vertex] - visited)
	return [visited, metavisited]
	
def connected_components(matrix, author_to_int):
	#convert matrix to adj_list
	v = len(matrix)
	adj_list = convert_matrix_to_adj_list(matrix, v)
	#using dfs to find connected components
	metavisited, list_of_ints = [False for _ in range(v)], []

	for vertex in range(v):
		if not metavisited[vertex]:
			ret = dfs(metavisited, vertex, adj_list)
			list_of_ints.append(ret[0])
			metavisited = ret[1]

	largest = largest_connected(list_of_ints)
	max_cc_size, max_cc, sizes = largest[0], largest[1], sorted(largest[2])

	#convert ints into authors
	inverse_author_dict = {v: k for k, v in author_to_int.items()}
	list_of_strings, max_cc_string = [], []
	for cc in list_of_ints:
		string_cc = [inverse_author_dict[i] for i in cc]
		if cc == max_cc:
			max_cc_string = string_cc
		list_of_strings.append(string_cc)

	#statistics of cc sizes
	average = statistics.mean(sizes)
	median = statistics.median(sizes)
	median_low = statistics.median_low(sizes)
	median_high = statistics.median_high(sizes)
	mode = calc_mode(sizes)
	#density per connected component
	d_per_component = density_per_component(list_of_ints, matrix, author_to_int)
	#saving info into a text file
	with open('connected_components.txt', 'w') as f: 
		f.write('Connected authors: ' + '\n')
		for cc in list_of_strings:
			f.write('\n' + str(len(cc)) + '   ' + str(cc) + '\n')
			f.write('Density : ' + str(d_per_component[str(cc)]) + '\n')
		f.write('\n')
		f.write('Connected components: ' + '\n')
		for cc in list_of_ints:
			f.write(str(len(cc)) + '   ' + str(cc) + '\n')
		f.write('\n')
		f.write('Number of connected components: ' + str(len(list_of_ints)) + '\n')
		f.write('Largest component size: ' + str(max_cc_size) + '\n')
		f.write('Largest connected component: ' + str(max_cc_string) + '\n')
		f.write('Component sizes: ' + str(sizes) + '\n')
		f.write('Average component size: ' + str(average) + '\n')
		f.write('Median: ' + str(median) + '\n')
		f.write('Low median: ' + str(median_low) + '\n')
		f.write('High median: ' + str(median_high) + '\n')
		f.write('Mode: ' + str(mode))
	pickle.dump(adj_list, open("adj_list.p", "wb"))
	pickle.dump(list_of_ints, open("list_of_ints.p", "wb"))

def convert_matrix_to_adj_list(matrix, size):
	adj_list = []
	for i in range(size):
		neighbors = set()
		for j in range(size): 
			if matrix[i][j] == 1:
				neighbors.add(j)
		adj_list.append(neighbors)
	return adj_list

def largest_connected(list_of_ints):
	sizes, s = dict(), []
	for list in list_of_ints:
		i = len(list) 
		sizes[i] = list
		s.append(i)
	m = max(sizes.keys())
	return [m, sizes[m], s]

def density(matrix):
	e = 0
	v = len(matrix)
	for i in range(v):
		for j in range(v): 
			if matrix[i][j] == 1:
				e += 1
	d = (e) / (v*(v-1))
	print('Density: ' + str(d) + '\n')
	# d = 0.017539133818203587

def author_degrees(matrix, author_to_int):
	stats = dict()
	v = len(matrix)
	sorted_authors = sorted(author_to_int, key=author_to_int.get)
	for key in sorted_authors:
		stats[key] = 0
	for i in range(v):
		for j in range(v): 
			if matrix[i][j] == 1:
				stats[sorted_authors[i]] += 1
				
	with open('author_degrees.csv', 'wt', newline='') as csvf:
		writer = csv.writer(csvf)
		writer.writerow(['Author', 'Degrees'])
		for key in sorted(stats, key=stats.get):
			writer.writerow([key, str(stats[key])])

def authors_per_paper(author_matrix):
	linelengths = [len(paper) for paper in author_matrix]	
	with open('authors_per_paper.csv', 'wt', newline='') as csvf:
		writer = csv.writer(csvf)
		writer.writerow(['Paper', 'Number of Authors'])
		for i in range(len(linelengths)):
			writer.writerow([str(i), str(linelengths[i])])

def calculate_metrics():
	try: 
		sys.stdout = open('console_verbose.txt', 'w')
		author_to_int = pickle.load(open("author_int_dict.p", "rb"))
		matrix = pickle.load(open("adjacency_matrix.p", "rb"))
		author_matrix = pickle.load(open("author_matrix.p", "rb"))
		global G
		G = graph.generate_networkX_graph_string()

		density(matrix)
		authors_per_paper(author_matrix)
		diameter(matrix)
		author_degrees(matrix, author_to_int)
		connected_components(matrix, author_to_int)
		cut_point(author_to_int)
		clustering_coefficient()
		betweenness_centrality()
		closeness_centrality()
		sys.stdout.close()
	except FileNotFoundError as err:
		pass