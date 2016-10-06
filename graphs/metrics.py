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
				# no need to check if j is in cc
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

def get_overall_stats(results_dict):
    average = statistics.mean(results_dict)
    median = statistics.median(results_dict)
    median_low = statistics.median_low(results_dict)
    median_high = statistics.median_high(results_dict)
    mode = calc_mode(results_dict)
    return {'avg': average, 'med': median, 'medlo': median_low, 'medhi': median_high, 'mode': mode}

def write_overall_stats(filename, stats):
    with open(filename, 'w') as f:
    	f.write('\nAverage: ' + str(stats['avg']) + '\n')
    	f.write('Median: ' + str(stats['med']) + '\n')
    	f.write('Median low: ' + str(stats['medlo']) + '\n')
    	f.write('Median high: ' + str(stats['medhi']) + '\n')
    	f.write('Mode: ' + str(stats['mode']) + '\n')

def write_author_stats(filename, centrality, result):
    with open(filename, 'wt', newline='') as csvf:
    	writer = csv.writer(csvf)
    	writer.writerow(['Author', centrality])
    	for author in sorted(result, key=result.get):
    		writer.writerow([author, str(result[author])])

def get_stats(results_dict):
    sorted_results_dict = sorted(results_dict, key=results_dict.get)
    stats = [results_dict[key] for key in sorted_results_dict]
    return stats

def betweenness_centrality():
    result = nx.betweenness_centrality(G)
    stats = get_stats(result)
    overall_stats = get_overall_stats(stats)
    write_overall_stats('betweenness_centrality.txt', overall_stats)
    write_author_stats('betweenness_centrality.csv', 'Betweenness Centrality', result)

def clustering_coefficient():
    result = nx.clustering(G)
    stats = get_stats(result)
    overall_stats = get_overall_stats(stats)
    write_overall_stats('clustering_coefficient.txt', overall_stats)
    write_author_stats('clustering_coefficient.csv', 'Clustering Coefficient', result)

def closeness_centrality():
    result = nx.closeness_centrality(G)
    stats = get_stats(result)
    overall_stats = get_overall_stats(stats)
    write_overall_stats('closeness_centrality.txt', overall_stats)
    write_author_stats('closeness_centrality.csv', 'Closeness Centrality', result)

def avg_pathlengths():
	pathlengths = []
	with open('averagepaths.txt', 'w') as f:
		for g in nx.connected_component_subgraphs(G):
			print(str(list(g)))
			if len(g) == 1:
				print('Skipped \n')
				continue
			fig = nx.average_shortest_path_length(g)
			pathlengths.append(fig)
			print(fig)
			f.write(str(list(g)) + '\n')
			f.write(str(fig) + '\n\n')
		avg = statistics.mean(pathlengths)
		f.write('Avg fig :' + str(avg))

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
		avg_pathlengths()
	except FileNotFoundError as err:
		pass
