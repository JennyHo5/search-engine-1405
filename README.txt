To run the crawler on a seed page:

1)Let the “seed” variable in “crawler-start.py” equals the URL of the seed page
	Eg. seed = "http://people.scs.carleton.ca/~davidmckenney/fruits/N-0.html"

2)enter this line in the command line: 
	python3 crawler-start.py

Then the crawler.py will crawl the URLs and save the required data in the current directory.

To run any test file:
1)run the crawler on a seed page from that database, since I’ve commented out the crawler.crawl() line to prevent duplicate crawls
2)run the test file
