
#script to give me more info about all the authors:

_f = open('authornames.txt', 'r')

authorList = []
lines = 0

for line in _f:
	lines += 1
	line.strip()
	arrLine = line.split(",")
	for authorname in arrLine:
		authorname.strip()
		authorList.append(authorname.strip('\n').lstrip())

_f.close()

lengthList = len(authorList)
print(lengthList)
print(lines)
print(authorList)

#turns out there is a total of 566 authors I need to analyze! 