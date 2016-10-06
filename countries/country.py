"""Generates tables about countries of publication and work. HCD+D Methods."""

import csv
import sys

def parsedata(filename, columns):
	""" Parses dataset.csv and pulls out relevant columns to text files."""

	with open('outpub.txt', 'w') as f:
		pub_columns = columns[:2]
		f.write(write_publish_data(filename, pub_columns))
	with open('outwork.txt', 'w') as f:
		f.write(write_work_data(filename, columns[2]))
	return ['outpub.txt', 'outwork.txt']

def write_publish_data(filename, pub_columns):
	with open(filename, 'r') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		for row in reader:
			retarr = []
			for item in pub_columns: 
				retarr.append(row[item])
			retval = " | ".join(retarr)
			yield retval + '\n'

def write_work_data(filename, column): 
	with open(filename, 'r') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		for row in reader:
			yield row[column] + '\n'

def publication(output):
	""" Create dictionaries of first author and rest of authors' countries of publication."""

	firstCountries = otherCountries = dict()
	done, skip = set(), 0
	with open(output, 'r') as f: 
		for line in f: 
			if skip < 2:
				skip += 1
				continue
			arrLine = line.split(' | ')
			firstC = arrLine[0].split(',')
			secC = arrLine[1].split(',')
			firstCountries = increment(firstC, firstCountries)
			otherCountries = increment(secC, otherCountries)

	write_publication_csv(firstCountries, otherCountries)

def increment(country_line, countries_dict):
	for country in country_line:
		country = country.lstrip().rstrip().strip('\n')
		if country in countries_dict:
			countries_dict[country] += 1
		else: 
			countries_dict[country] = 1
	return countries_dict

def write_publication_csv(firstCountries, otherCountries):
	with open('country-pub.csv', 'w', newline='') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(('Country', 'Number of First Authors', 'Number of Other Authors'))
		for key in firstCountries:
			if key in otherCountries:
				writer.writerow((key, firstCountries[key], otherCountries[key]))
			elif key not in otherCountries:
				writer.writerow((key, firstCountries[key], '0'))
			done.add(key)
		for key in otherCountries:
			if key not in done: 
				if key in firstCountries:
					writer.writerow((key, firstCountries[key], otherCountries[key]))
				elif key not in firstCountries:
					writer.writerow((key, '0', otherCountries[key]))
	print("Done! Look for <country-pub.csv> file in your directory.")

def work(output): 
	""" Creates dict of countries and their number of mentions as the place of work. """
	
	countries, skip = dict(), 0
	with open(output, 'r') as f: 
		for line in f: 
			if skip < 2:
				skip += 1
				continue
			arrLine = line.split(',')
			countries = increment(arrLine, countries)
	write_countries_csv(countries)

def write_countries_csv(countries):
	with open('country-work.csv', 'w', newline='') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(('Country', 'Number of Mentions as Place of Work'))
		for key in countries:
			writer.writerow((key, countries[key]))
	print("Done! Look for <country-work.csv> file in your directory.")

def main():
	"""Command line: python countries.py <path/to/dataset.csv>"""
	
	dataset = sys.argv[1]
	columns = [10, 12, 13]
	retval = parsedata(dataset, columns)
	publication(retval[0])
	work(retval[1])

if __name__ == "__main__":
	main()