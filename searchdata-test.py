
import webdev
import os
import json
import searchdata


URL = "http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html"

word = "banana"

print(searchdata.get_crawled_words())

if word in searchdata.get_crawled_words():
    print("True")

print(searchdata.get_idf(word))

print(searchdata.get_tf(URL, word))

print((searchdata.get_tf_idf(URL, word)))
