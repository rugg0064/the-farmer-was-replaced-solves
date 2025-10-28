# Comparators return true if A belongs before B

def mergeSort(list, comparator):
	#quick_print("starting", list)
	length = len(list)
	if length <= 1:
		#quick_print("returning early")
		return list
	a = []
	b = []
	AIndex = (len(list) - 1) // 2
	for i in range(length):
		if i <= AIndex:
			a.append(list[i])
		else:
			b.append(list[i])
	#quick_print("split into", a, b)
	a = mergeSort(a, comparator)
	b = mergeSort(b, comparator)
	#quick_print("recursive calls complete", a, b)
	i = 0
	j = 0
	ret = []
	#quick_print("merging", a, b)
	while (i+j) < length:
		#quick_print("merge step", i, j, ret)
		if i == len(a):
			ret.append(b[j])
			j += 1
		elif j == len(b):
			ret.append(a[i])
			i += 1
		elif comparator(a[i], b[j]):
			ret.append(a[i])
			i += 1
		else:
			ret.append(b[j])
			j += 1
	#quick_print("finished merge", ret)
	return ret

def sortedInsert(arr, value, comparator):
	if len(arr) == 0:
		arr.append(value)
		return
	for i in range(len(arr)):
		if comparator(value, arr[i]):
			arr.insert(i, value)
			return
	arr.append(value)

# returns true when a belongs before b
def numAscend(a, b):
	return a < b

# Returns a comparator function which is inverted from the one provided
def invert(comparator):
	def invertedComparator(a, b):
		return not comparator(a, b)
	return invertedComparator
	
def test():
	data = [
		("K", 999),
		("D", -15),
		("U", 45),
		("C", 90)
	]
	def sort(a, b):
		return numAscend(a[1], b[1])
	quick_print(mergeSort(data, sort))

def last(list):
	if len(list) == 0:
		return None
	return list[len(list)-1]
	
def copy(list):
	newList = []
	for value in list:
		newList.append(value)
	return newList