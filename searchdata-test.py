
import webdev
import os
import json
import searchdata

a = 0.1

threshold = 0.0001

URL = "http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-8.html"

print((searchdata.calculate_page_ranks(URL, a, threshold)).values())
