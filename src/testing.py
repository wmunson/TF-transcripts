# li = ['a','x','b','c','x','x','a','x','x','c','b','x','a','x']
# #	   0   1   2   3   4   5   6   7   8   9   10  11  12  13
# pr = ['a','b','c']
# d={'a':[],'b':[],'c':[]}

# pers = ''
# for i,l in enumerate(li):
# 	print(i)
# 	for p in pr:
# 		if p == l:
# 			pers = p
# 	try:
# 		d[pers].append(i)
# 	except KeyError:

# 		pass


# print(d)

import pandas as pd

data = pd.read_csv('links5.csv', sep="|")

# ep=(data['ep'])
# for i,n in enumerate(ep):
# 	if i+1 == n:
# 		print(n)
# 	# print(i+1,n)

guests = data.loc[data.urls.str.contains('.pdf') & (data.guests=='None')]

urls = (guests['urls'])
print(urls)

for _ in urls:
	print(_)