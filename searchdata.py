# produce data required by search engine
# test the correctness of the data produced through crawler module
# read information from the json docs and produce correct outputs

import crawler
import webdev
import os
import json
import matmult
import math

# return a dict of the data of all pages that have been crawled
def get_crawled_pages():
    crawled_pages = {}
    for filename in os.listdir():
        if filename.endswith("json"):
            filein = open(filename, "r")
            data = json.load(filein)
            crawled_pages[data["link"]] = data
            filein.close()
    return crawled_pages

# url -> title
def get_title(URL):
    crawled_pages = get_crawled_pages() # key -> url, value -> {link:..., title:..., ...}
    for key in crawled_pages:
        if key == URL:
            page_title = crawled_pages[key]["title"]
    return page_title


# return a dict including all of the words in crawled pages, key -> url, value -> words
def get_all_words():
    all_words = {}
    crawled_pages = get_crawled_pages() # a dict
    for url in crawled_pages:
        data = crawled_pages[url]
        for i in data:
            if i == "words":
                words = data[i]
                all_words[url] = words
    return all_words

# return a list including all words crawled (no duplication)
def get_crawled_words():
    crawled_words = []
    for url in get_all_words():
        words = get_all_words()[url]
        for i in words:
            if i not in crawled_words:
                crawled_words.append(i)
    return crawled_words

# return a list of all the URLs that have been crawled
def get_crawled_links():
    crawled_links = []
    crawled_pages = get_crawled_pages()
    for page in crawled_pages:
        crawled_links.append(page)
    return crawled_links


# URL -> a list of other URLs that the page with the given URL links to
def get_outgoing_links(URL):
    crawled_links = get_crawled_links()
    # 1. if the URL was not found during the crawling process then return None
    if URL not in crawled_links:
        return None
    # 2. read the html on the page
    html = webdev.read_url(URL)
    # 3. find the links in the html
    outgoing_links = crawler.find_links(html, URL)
    return outgoing_links

#URL - > a list of URLs for pages that link to the page with the given URL
def get_incoming_links(URL):
    crawled_links = get_crawled_links()
    # 1. if the URL was not found during the crawling process then return None
    if URL not in crawled_links:
        return None
    # 2. if the URL is in the list of the outgoing links of another URL, then include that another URL into the list
    incoming_links = []
    crawled_pages = get_crawled_pages()
    for page in crawled_pages:
        # if it is the same page, skip
        if URL == page:
            continue
        # if the links in the page include the current URL, store the page's link into incoming_links
        if URL in crawled_pages[page]["links"]:
            incoming_links.append(page)
    return incoming_links


# calculate the pagerank
def calculate_page_ranks(URL):
    a = 0.1
    threshold = 0.0001
    crawled_links = get_crawled_links() # there are N pages crawled
    # 1. if the URL was not found during the crawling process then return None
    if URL not in crawled_links:
        return None

    # 2. match each link to an interger
    int_links = {}
    for i in range(len(crawled_links)):
        int_links[i] = crawled_links[i]

    # get the specific integer for a page
    def get_int(URL):
        for int, link in int_links.items():
            if link == URL:
                page_int = int
        return page_int

    # turn integer into the original URL
    def get_url(integer):
        for int, link in int_links.items():
            if int == integer:
                URL = link
        return URL

    # 3. create a N*N matrix
    matrix = []
    N = len(int_links)
    for i in range(N):
        matrix.append([])
        for j in range(N):
            matrix[i].append(0)

    # figure out if two links have connections
    def if_connect(URL_1, URL_2):
        URL_1_outgoing_links = get_outgoing_links(URL_1)
        URL_1_incoming_links = get_incoming_links(URL_1)
        if (URL_2 in URL_1_outgoing_links) or (URL_2 in URL_1_incoming_links):
            return True
        else:
            return False

    # 4. the number at [i, j] = 1 if node i links to node j; = 0 otherwise
    for i in range(N):
        URL_i = get_url(i)
        for j in range(N):
            URL_j = get_url(j)
            if if_connect(URL_i, URL_j) == True:
                matrix[i][j] = 1


    # 5 sort the rows: has no 1s / has 1s
    row_has_no_1 = []
    row_has_1 = []

    for i in range(N):
        for j in range(N):
            if matrix[i][j] == 1:
                row_has_1.append(i)
                break
            if j == N - 1: # reach the end of the row that has no 1s
                row_has_no_1.append(i) # append the row to the row_has_no_1 list

    # 6. if a row has no 1s, replace each element in that row by 1/N
    for row in range(N):
        if row not in row_has_no_1:
            continue
        for col in range(N):
            matrix[row][col] == 1/N


    # 7. in other rows, divide each 1 by number of 1s in that row
    for row in range(N):
        sum = 0
        if row not in row_has_1:
            continue
        for col in range(N):
            if matrix[row][col] == 1:
                sum += 1
        for col in range(N):
            if matrix[row][col] == 1:
                matrix[row][col] = 1/sum

    # 7. multiply the resulting matrix by (1 - a)
    matrix = matmult.mult_scalar(matrix, (1 - a))

    # 8. add a/N to each entry of the resulting matrix
    for i in range(N):
        for j in range(N):
            matrix[i][j] += a/N


    # 9. keep multiplying the matrix by a vector π (1, 0, 0, ...) until difference in π between iterations is below a threshold
        # 9.1 create a vector
    v0 = [[]]
    for i in range(N):
        v0[0].append(1/N)

        # 9.2  keep multiplying the matrix by a vector π (1, 0, 0, ...) until difference in π between iterations is below a threshold

    e = 1
    while e >= threshold:
        v1 = matmult.mult_matrix(v0, matrix)
        e = matmult.euclidean_dist(v0, v1)
        v0 = v1

    # 10. return pageranks for all pages
    page_ranks = {}
    for i in range(N):
        page_ranks[int_links[i]] = v0[0][i]

    return page_ranks


# URL -> the PageRank value of the page with that URL
# what PageRank calculates: the probability the random surfer is on page x at any given time
def get_page_rank(URL):
    crawled_links = get_crawled_links()
    # 1. if the URL was not found during the crawling process then return None
    if URL not in crawled_links:
        return None
    # 2. calculate the page rank
    ranks = calculate_page_ranks(URL)
    for key in ranks:
        if key == URL:
            rank = ranks[key]
    return rank

# Accepts a single string argument representing a word and returns the inverse document frequency of that word within the crawled pages
def get_idf(word):
    # create a list that include all word crawled (no duplicate)
    crawled_words = get_crawled_words()

    # 1. if the word was not present in any crawled documents, this function must return 0
    if word not in crawled_words:
        return 0

    # 2. else, calculate frequency
        # 2.1 total document
    total_docs_num = len(get_crawled_pages())
        # 2.2 number of documents w appears in
    appear_num = 0
    for key in get_all_words():
        url = key
        page_words = get_all_words()[key] # return a list of words on page
        if word in page_words:
            appear_num += 1
        # 2.3 calculate the frequency
    numerator = total_docs_num
    denominator = 1 + appear_num
    fraction = numerator / denominator
    idf = math.log(fraction, 2)
    return idf

# Accepts two string arguments: a URL and a word. This function must return the term frequency of that word within the page with the given URL
def get_tf(URL, word):
    # 1. If the word does not appear in the page with the given URL, or the URL has not been found during the crawl, this function must return 0
        # 1.1 if the URL does not found during the crawl, returin 0
    if URL not in get_crawled_links():
        return 0

        # 1.2 if the word does not appear in the page with the given URL, return 0
    curr_words = get_all_words()[URL]
    if word not in curr_words:
        return 0

    # 2. claculate tf
        # 2.1 occurences of word in doc
    count = 0
    for i in curr_words:
        if i == word:
            count += 1
    numerator = count
    denominator = len(curr_words)
    tf = numerator / denominator
    return tf

# return the tf-idf weight for the given word within the page represented by the given URL
def get_tf_idf(URL, word):
    tf = get_tf(URL, word)
    idf = get_idf(word)
    tf_idf = math.log(1 + tf, 2) * idf
    return tf_idf
