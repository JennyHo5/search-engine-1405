import crawler
import json
import time

seed = "http://people.scs.carleton.ca/~davidmckenney/fruits/N-0.html"

start = time.time()
crawler.crawl(seed)
end = time.time()
print("Crawl time:", (end-start))
