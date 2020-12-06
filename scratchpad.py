from functools import reduce


l = ['abc', 'ac', 'aqq']

ls = [set(x) for x in l]
print(reduce(lambda x, y: x.intersection(y), ls))
