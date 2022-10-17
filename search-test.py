import search


URL = "http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html"

phrase = "I am an apple peach"
boost = True

print(search.search(phrase, boost))
