"""A script that parses list of authors, creating a CSV file ordering
authors by their positions. """

import csv 

_f = open('authornames.txt', 'r')
# L = [18][163]

authorDict = {}

for line in _f:
	line.rstrip()
	position = 1
	arrLine = line.split(",")
	for authorname in arrLine:
		if position in authorDict:  	
			authorDict[position].append(authorname.strip('\n').lstrip()) 
		else:
			authorDict[position] = [authorname.strip('\n').lstrip()]	
		counter += 1

_f.close()

# f = open('author-organized.csv', 'wt')
# writer = csv.writer(f)
# writer.writerow(('Article', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18'))
# for i in range(len(all_course_codes)):
#     writer.writerow((all_course_codes[i], all_course_titles[i], all_course_descriptions[i]))
# f.close()


result_file = open('authors.txt', 'w+')

for key in sorted(authorDict.keys()):
	result_file.write('\n' + '============================ ' + str(key) + ' authors =============================\n')
	for author in authorDict[key]:
		result_file.write(author + '\n')

result_file.close()
