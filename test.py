l1 = []

d1 = {'A':10,'B':20,'C':10}

for i , j in d1.items():
	l1.append((i,j))
	# l1 = list(set(l1))

print(l1)

for i in l1:
	print(i[0])
	print(l1.index(i))

print("######")
# import json

# x  = open('intents.json').read()
# y = json.loads(x)
# print(type(y))


