
import webdev
import os
import json
import searchdata


URL = "http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-8.html"

print((searchdata.calculate_page_ranks(URL).values()))
