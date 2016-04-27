import csv
import sys
import getopt

""" This is a snippet of code I wrote to regenerate the authors.txt file after deleting it.
"""
# f = open('finalauthors.txt', 'w+')
# with open('separated-authors.csv', 'r') as csvfile:
# 	reader = csv.reader(csvfile, delimiter=',')
# 	for row in reader:
# 		line = row[0]
# 		for i in range(1, 11):
# 			line = line + ', ' + row[i]
# 		print(line)
# 		f.write(line + '\n')
# f.close()

def parsedata(filename, columns):

	""" Parses dataset and pulls out relevant columns from the csv data file to text file. 

		@param args: 
					filename, a string with the path to the csv data file
					output, string with path to desired output text file
					columns, a list of columns in csv data file to be extracted 
		@param output:  
					string path to text file with desired information 
	"""

	with open('out.txt', 'w') as f:
		with open(filename, 'r') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			for row in reader:
				if len(columns) > 1:
					retarr = []
					for item in columns: 
						retarr.append(row[item])
					retval = " | ".join(retarr)
					f.write(retval + '\n')
					print(retval)
				else:
					f.write(row[columns[0]] + '\n')
					print(row[columns[0]])
	print("Done! Look for <out.txt> file in your directory.")
	return 'out.txt'


def publication(output):

	""" Creates a CSV table of countries, number of first authors who published there,
		and number of other authors who published there. 

		@param args: 
					output, a string with the path to the text file output by parsedata
					csvfilename, user specified string with the path to new csv file

		@param output: 
					a csv file with desired analysis
					prints string path to csv file 
	"""

	firstCountries = dict()
	otherCountries = dict()
	check = set()
	count = 0
	verify = True

	with open(output, 'r') as f: 
		for line in f: 
			if verify: 
				count += 1
				verify = False
				continue
				
			if count == 1: 
				count = 0
				continue

			arrLine = line.split(' | ')
			firstC = arrLine[0].split(',')
			secC = arrLine[1].split(',')

			for _ in firstC:
				_ = _.lstrip().rstrip().strip('\n')
				if _ in firstCountries:
					firstCountries[_] += 1
				else: 
					firstCountries[_] = 1

			for _ in secC:
				_ = _.lstrip().rstrip().strip('\n')
				if _ in otherCountries:
					otherCountries[_] += 1
				else: 
					otherCountries[_] = 1

		print(firstCountries)
		print(otherCountries)


	with open('countries-pub.csv', 'w', newline='') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(('Country', 'Number of First Authors', 'Number of Other Authors'))

		for key in firstCountries:
			if key in otherCountries:
				writer.writerow((key, firstCountries[key], otherCountries[key]))
			elif key not in otherCountries:
				writer.writerow((key, firstCountries[key], '0'))
			check.add(key)

		for key in otherCountries:
			if key not in check: 
				if key in firstCountries:
					writer.writerow((key, firstCountries[key], otherCountries[key]))
				elif key not in firstCountries:
					writer.writerow((key, '0', otherCountries[key]))

	print("Done! Look for <countries-pub.csv> file in your directory.")


def work(output): 

	""" Creates a CSV table of countries and their number of mentions as the place of work in a paper. 

		@param args: 
					output, a string with the path to the text file output by parsedata
					csvfilename, user specified string with the path to new csv file

		@param output: 
					a csv file with desired analysis
					prints the string path to csv  
	"""

	countries = dict()
	verify = True
	count = 0

	with open(output, 'r') as f: 
		for line in f: 
			if verify: 
				verify = False
				count += 1
				continue

			if count == 1: 
				count = 0
				continue

			arrLine = line.split(',')
			for _ in arrLine:
				_ = _.lstrip().rstrip().strip('\n')
				if _ in countries:
					countries[_] += 1
				else: 
					countries[_] = 1

	with open('countries-work.csv', 'w', newline='') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(('Country', 'Number of Mentions as Place of Work'))
		for key in countries:
			writer.writerow((key, countries[key]))

	print("Done! Look for <countries-work.csv> file in your directory.")


def main():

	""" Function to parse command line input. 
	    Expects csv filename, columns, and either work or publication. 
	    On the command line: python countries.py <dataset.csv> <[col,col]> <work or publication>
	    Columns within the csv file are 0-indexed. 
	    Make sure there are no spaces when specifying your desired columns. 
	"""
	try:
		opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
	except getopt.error as msg:
		print (msg)
		print ("for help use --help")
		sys.exit(2)
    # process options
	for o, a in opts:
		if o in ("-h", "--help"):
			print (__doc__)
			sys.exit(0)
    # process arguments
	col = args[1].strip('[').strip(']')
	arrCol = col.split(',')
	columns = [int(x) for x in arrCol]
	dataset = args[0]
	option = args[2]
	    
	#returns string path to output text file
	retval = parsedata(dataset, columns)
	if option == "work":
	  	work(retval)
	elif option == "publication":
		publication(retval)
	
	# for arg in args:
	#     process(arg) # process() is defined elsewhere

if __name__ == "__main__":
	main()