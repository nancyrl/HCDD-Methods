import csv
import pickle
import os

path_to_dataset = 'C:/Users/Nancy/HCD+D/HCDD-Methods/dataset.csv'
path_to_authors = 'C:/Users/Nancy/HCD+D/HCDD-Methods/graphs/sepauthors.csv'
path_to_graphs = 'C:/Users/Nancy/HCD+D/HCDD-Methods/graphs/'
years_papers_dict = {}

def generate_paper_years_dict():
	with open(path_to_dataset, 'r') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		skip, count = 0, 0
		for row in reader:
			while skip < 2:
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
	for year in years_papers_dict:
		write_authors_text_file(year, years_papers_dict[year])

def write_authors_text_file(year, papers):
	lines = []
	with open(path_to_authors, 'r') as f:
		reader = csv.reader(f, delimiter=',') 
		count = 0
		for row in reader:
			if 'First Author' in row:
				continue
			if count in papers: 
				new_row = [item for item in row if item]
				lines.append(new_row)
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

def main():
	generate_paper_years_dict()
	generate_author_txt_by_years()
                
if __name__ == "__main__":
    main()
