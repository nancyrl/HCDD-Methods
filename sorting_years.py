import csv
import pickle
import os

path_to_dataset = 'C:/Users/Nancy/HCD+D/HCDD-Methods/graphs/not2015/dataset2015.csv'
path_to_authors = 'C:/Users/Nancy/HCD+D/HCDD-Methods/graphs/not2015/sepauthors2015.csv'
path_to_graphs = 'C:/Users/Nancy/HCD+D/HCDD-Methods/graphs/'
years_papers_dict = {}

def generate_paper_years_dict():
	with open(path_to_dataset, 'r') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		skip, count = 0, 0
		for row in reader:
			if skip < 2:
				skip += 1
				continue
			if row[3] == "":
				break
			key = int(row[3])
			if key not in years_papers_dict:
				years_papers_dict[key] = [count]
			else:
				years_papers_dict[key].append(count)
			count += 1

def generate_author_txt_by_years():
	dict_array = sorted(years_papers_dict)
	print(dict_array)
	for i in range(len(dict_array)):
		total_papers = []
		if i != 0: 
			for j in range(i):
				total_papers.append(years_papers_dict[dict_array[j]])
		total_papers.append(years_papers_dict[dict_array[i]])
		write_authors_text_file(dict_array[i], total_papers)

def write_authors_text_file(year, papers):
	lines, npapers = [], []
	for paper in papers:
		for i in range(len(paper)):
			npapers.append(paper[i])
			
	with open(path_to_authors, 'r') as f:
		reader = csv.reader(f, delimiter=',') 
		count = 0
		for row in reader:
			if 'First Author' in row:
				continue
			if count in npapers: 
				lines.append([item for item in row if item])
			count += 1

	# make a directory for each year
	path = path_to_graphs + str(year)
	os.makedirs(path, exist_ok=True)
	text_file = path + '/authors' + str(year) + '.txt'
	with open(text_file, 'w') as f:
		for line in lines:
			str_line = str(line).strip('[').strip(']').translate(str.maketrans({"'":None})) 
			print(str_line)
			f.write(str_line + '\n') 
	print("Made " + text_file)

generate_paper_years_dict()
generate_author_txt_by_years()