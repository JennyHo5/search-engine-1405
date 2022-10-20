# For this question, you will implement an improved queue-like data structure that uses more memory space (i.e., stores more data), but allows us to insert, remove, and determine if an item is present in constant time, while also maintaining the order of item insertion.

#  adding an element to the end of a list
def addend(list, dict, value):
	list.append(value)
	# add the new item to the dict
	if value not in dict:
		dict[value] = 0
	dict[value] += 1

# removing an element from the start
def removestart(list, dict):
	if len(list) == 0:
		return None

	first_item = list[0]

	# remove the value in the dict
	if first_item in dict:
		if dict[first_item] == 1:
			del dict[first_item]
		else:
			dict[first_item] -= 1

	return list.pop(0)


# adding an additional function, called containshash(dict, value), that will determine if an item exists in the list in O(1) time
def containshash(dict, value):
	# find the "value" in the dict, AKA the key in the dict
	if value in dict.keys():
		return True
	else:
		return False


# start = time.time()
# for i in searchlist:
# 	containslinear(list, i)
# end = time.time()
# print("Linear time: ", (end-start))
#
# start = time.time()
# for i in searchlist:
# 	containshash(hash, i)
# end = time.time()
# print("Hash time: ", (end-start))
