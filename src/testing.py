li = ['a','x','b','c','x','x','a','x','x','c','b','x','a','x']
#	   0   1   2   3   4   5   6   7   8   9   10  11  12  13
pr = ['a','b','c']
d={'a':[],'b':[],'c':[]}

pers = ''
for i,l in enumerate(li):
	print(i)
	for p in pr:
		if p == l:
			pers = p
	try:
		d[pers].append(i)
	except KeyError:

		pass


print(d)