
import webdev
import os
import json
import searchdata

a = 0.1

URL = "http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html"

print(searchdata.calculate_page_rank(URL, a))
