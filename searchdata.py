# produce data required by search engine
# test the correctness of the data produced through crawler module
# read information from the json docs and produce correct outputs

import crawler
import webdev
import os
import json
import matmult

# return a list of the data of all pages that have been crawled
def get_crawled_pages():
    crawled_pages = {}
    for filename in os.listdir():
        if filename.endswith("json"):
            filein = open(filename, "r")
            data = json.load(filein)
            crawled_pages[data["link"]] = data
            filein.close()
    return crawled_pages

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
    ranks = calculate_page_ranks(URL, a, threshold)
    for key in ranks:
        if key == URL:
            rank = ranks[key]
    return rank
