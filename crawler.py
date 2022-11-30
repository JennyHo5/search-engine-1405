# perform the web crawling

import webdev
import json
import os
import improved_queue
import matmult
import math
# the improved_queue module that can insert, remove, and determine if an item is present in the queue in O(1) time, while also maintaining the order of item insertion
# addend(list, dict, value), removestart(list, dict), containshash(dict, value)

def find_title(str):
    start_title_tag_index = str.find("<title")
    end_title_tag_index = str.find("</title>") # depends on the length of <title> tag
    title_tag = str[start_title_tag_index + 6 : end_title_tag_index]
    start_title_index = title_tag.find(">") + 1
    title = title_tag[start_title_index :]
    return title

def find_words(str):
    all_words = []
    while "<p" in str:
        start_p_index = str.find("<p") # depends on the length of previous string
        end_p_index = str.find("</p>") # depends on the length of <p> tag
        p = str[start_p_index : end_p_index]
        start_words_index = p.find(">") + 1
        words = p[start_words_index :]
        words = words.split()
        for word in words:
            all_words.append(word)
        # delete the saved p and find the next new p
        str = str[: start_p_index] + str[end_p_index + 4:]
    return all_words

#determine if it is a relative or absolute link, and return the full URL
def rel_or_abs(link, seed):
    start_rel_index = seed.rindex("/") # find the index of the last "/"
    cur = seed[: start_rel_index]
    if link.startswith("http://") == True:
        return link
    else:
        link = cur + link[1:]
        return link

def find_links(html, seed):
    links = []
    while '<a href="' in html:
        start_a_index = html.find('<a href="') # depends on the length of previous string
        end_a_index = html.find('</a>') # depends on the length of <a> tag
        a = html[start_a_index + 9 : end_a_index]
        end_quotation_index = a.find('">')
        link = a[: end_quotation_index]
        link = rel_or_abs(link, seed)
        links.append(link)
        html = html[: start_a_index] + html[end_a_index + 5:]
    return links



def get_crawled_links(crawled_pages):
    crawled_links_hash = {} # this is dict used to do dictionary search O(1)
    crawled_links_list = [] # this is a list used to track the order
    for page in crawled_pages:
        improved_queue.addend(crawled_links_list, crawled_links_hash, page)
    return crawled_links_list, crawled_links_hash # result[0] and [1]


# return a dict including all of the words in crawled pages, key -> url, value -> words
def get_all_words(crawled_pages):
    all_words = {}
    for url in crawled_pages:
        data = crawled_pages[url]
        for i in data:
            if i == "words":
                words = data[i]
                all_words[url] = words
    return all_words



# return a list including all words crawled (no duplication), save it into a json file
def get_crawled_words(all_words):
    crawled_words = []
    for url in all_words:
        words = all_words[url]
        for i in words:
            if i not in crawled_words:
                crawled_words.append(i)
    return crawled_words


# map each URL that has been crawled to a specific int, and create a dictionary to contain those ints and URLs
def map_int_link(crawled_links_list):
    # 1. match each link to an interger
    int_links = {}
    for i in range(len(crawled_links_list)):
        int_links[i] = crawled_links_list[i]
    return int_links


# turn integer into the original URL
def get_url(integer, int_links):
    for int, link in int_links.items():
        if int == integer: #O(1)
            URL = link
    return URL

# URL -> a list of other URLs that the page with the given URL links to
# this is used for the if_connect(URL_1, URL_2) function
def get_outgoing_links(URL, crawled_links_hash):
    outgoing_links_hash = {}
    # 1. if the URL was not found during the crawling process then return None
    if URL not in crawled_links_hash: # O(n)
        return None
    # 2. read the html on the page
    html = webdev.read_url(URL)
    # 3. find the links in the html
    outgoing_links_list = find_links(html, URL)
    for link in outgoing_links_list:
        outgoing_links_hash[link] = 1
    return outgoing_links_hash

#URL - > a list of URLs for pages that link to the page with the given URL
# this is used for the if_connect(URL_1, URL_2) function
def get_incoming_links(URL, crawled_links_hash, crawled_pages):
    # 1. if the URL was not found during the crawling process then return None
    if URL not in crawled_links_hash: # O(n)
        return None
    # 2. if the URL is in the list of the outgoing links of another URL, then include that another URL into the list
    incoming_links = {}
    for page in crawled_pages:
        # if it is the same page, skip
        if URL == page:
            continue
        # if the links in the page include the current URL, store the page's link into incoming_links
        if URL in crawled_pages[page]["links"]:
            incoming_links[page] = 1
    return incoming_links

# figure out if two links have connections
def if_connect(URL_1, URL_2, URL_1_outgoing_links, URL_1_incoming_links, crawled_links_hash, crawled_pages):
    # URL_1_outgoing_links = get_outgoing_links(URL_1, crawled_links_hash) # a dict
    # URL_1_incoming_links = get_incoming_links(URL_1, crawled_links_hash, crawled_pages) # a dict
    if (URL_2 in URL_1_outgoing_links) or (URL_2 in URL_1_incoming_links): # O(1)
        return True
    else:
        return False


# get the information about wheather every two pages are connected
def get_url1_url2_connect(crawled_links_list, crawled_links_hash, crawled_pages):

    # save the if-connect data into a json files
    url1_url2_if_connect = {}
    for url1 in crawled_links_list:
        URL_1_outgoing_links = get_outgoing_links(url1, crawled_links_hash) # a dict
        URL_1_incoming_links = get_incoming_links(url1, crawled_links_hash, crawled_pages) # a dict
        url1_url2_if_connect[url1] = {}
        for url2 in crawled_links_list:
            if url2 == url1:
                continue
            if if_connect(url1, url2, URL_1_outgoing_links, URL_1_incoming_links, crawled_links_hash, crawled_pages) == True:
                url1_url2_if_connect[url1][url2] = True
            else:
                url1_url2_if_connect[url1][url2] = False
    return url1_url2_if_connect



# calculate the pageranks for all pages
def calculate_page_ranks(crawled_links_list, crawled_pages, int_links, urls_if_connect):
    a = 0.1
    threshold = 0.0001

    # 2. create a N*N matrix
    matrix = []
    N = len(crawled_links_list)
    for i in range(N):
        matrix.append([])
        for j in range(N):
            matrix[i].append(0)

    # 3. for the number at [i, j] = 1, if node i links to node j, then [i, j] = 1; otherwise = 0
    for i in range(N):
        URL_i = get_url(i, int_links)
        for j in range(N):
            URL_j = get_url(j, int_links)
            if URL_i == URL_j:
                continue
            if (urls_if_connect[URL_i][URL_j] == True) or (urls_if_connect[URL_j][URL_i] == True):
                matrix[i][j] = 1

    # 4. sort the rows: has no 1s / has 1s
    row_has_no_1 = []
    row_has_1 = []

    for i in range(N):
        for j in range(N):
            if matrix[i][j] == 1:
                row_has_1.append(i)
                break
            if j == N - 1: # reach the end of the row that has no 1s
                row_has_no_1.append(i) # append the row to the row_has_no_1 list

    # 5. if a row has no 1s, replace each element in that row by 1/N
    for row in range(N):
        if row not in row_has_no_1:
            continue
        for col in range(N):
            matrix[row][col] == 1/N


    # 6. in other rows, divide each 1 by number of 1s in that row
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

    while e > threshold:
        v1 = matmult.mult_matrix(v0, matrix)
        e = matmult.euclidean_dist(v0, v1)
        v0 = v1

    # 10. return pageranks for all pages
    page_ranks = {}
    for i in range(N):
        page_ranks[int_links[i]] = v0[0][i]

    return page_ranks



# calculate idfs for all words
# accepts a single string argument representing a word and returns the inverse document frequency of that word within the crawled pages
def calculate_idfs(crawled_pages, crawled_words, all_words):
    word_idf = {}
    # 1. total document
    total_docs_num = len(crawled_pages)
    # 2. number of documents w appears in
    for word in crawled_words: # O(n), n = number of words crawled
        appear_num = 0
        for key in all_words: # O(n), n = number of pages crawled
            url = key
            page_words = all_words[key] # return a list of words on page
            if word in page_words: # O(n), n = number of words on the specific page
                appear_num += 1
            # 2.3 calculate the frequency
        numerator = total_docs_num
        denominator = 1 + appear_num
        fraction = numerator / denominator
        idf = math.log(fraction, 2)
        word_idf[word] = idf
    return word_idf

# calculate tfs for all words and documents
# Accepts two string arguments: a URL and a word. This function must return the term frequency of that word within the page with the given URL
def calculate_tfs(crawled_pages, crawled_words, all_words):
    url_word = {} # a dicts of url_word_tfs dicts
    for page in crawled_pages:
        url = page
        url_word_tfs = {} # tfs for words to that specific url
        curr_words = all_words[url] # N(1)
        for word in crawled_words: # O(n), n = number of words crawled
            if word not in curr_words: # O(m), m = number of words on the specific page
                tf = 0
            else:
                count = 0
                for i in curr_words: # O(m), m = number of words on the specific page
                    if i == word:
                        count += 1
                numerator = count
                denominator = len(curr_words)
                tf = numerator / denominator
            url_word_tfs[word] = tf
        url_word[url] = url_word_tfs
    return url_word



def crawl(seed):


    # 1. Reset any existing data
    # delete all files and information from previous crawl

    curr_dir = os.getcwd()
    cache_dir = curr_dir + "/__pycache__"

    # 1.1 delete all the json files that represent each HTML in the current directory (don't delete the crawled-pages.json file)
    for filename in os.listdir(curr_dir):
        if filename.endswith("json"):
            os.remove(filename)

    # 1.2 clean cache
    for file in os.listdir(cache_dir):
        os.remove(os.path.join(cache_dir, file))
    os.rmdir(cache_dir)

    # 2. perform a web crawl starting at seed URL
        # 2.1 create a list of URLs that we need to visit
    queue_list = []
    queue_hash = {}

    already_crawled_list = [] # a list to track the page that we've already crawled so that we can skip them
    already_crawled_hash = {}

        # 2.2 add the initial URL to the queue
    improved_queue.addend(queue_list, queue_hash, seed)

    crawled_pages = {} #make a dict to save all crawled pages

        # 2.3 repeat until the queue is empty
    while len(queue_list) != 0:

            # 2.3.1 get the next URL from the queue
        link = improved_queue.removestart(queue_list, queue_hash)


        # if the page has already crawled, skip it
        if improved_queue.containshash(already_crawled_hash, link):
            continue


            # 2.3.2 read the current page (using webdev module)
        curr_page = {} # save the data from current page as a dict
        html = webdev.read_url(link)
        title = find_title(html)
        words = find_words(html)
        links = find_links(html, seed)
        curr_page["link"] = link
        curr_page["title"] = title
        curr_page["words"] = words
        curr_page["links"] = links


        for i in links: # add those links to the queue
            improved_queue.addend(queue_list, queue_hash, i)


        crawled_pages[link] = curr_page



        # add current page to the list "already_crawled"
        improved_queue.addend(already_crawled_list, already_crawled_hash, link)



    # 3. save crawled data to json files
    # write the crawled_pages dictionary into a json file
    fileout = open("crawled-pages.json", "w")
    data = json.dumps(crawled_pages, indent=4)
    fileout.write(data)
    fileout.close()

    # set the var crawled_pages
    filein = open("crawled-pages.json", "r")
    crawled_pages = json.load(filein) #(need updated) I don't need to load all of the crawled pages
    filein.close()


    #save crawled links (list) into a json file
    crawled_links_list_object = json.dumps(get_crawled_links(crawled_pages)[0], indent=4)
    fileout = open("crawled-links-list.json", "w")
    fileout.write(crawled_links_list_object)
    fileout.close()

    # set the var crawled_links_list
    filein = open("crawled-links-list.json", "r")
    crawled_links_list = json.load(filein)
    filein.close()

    #save crawled links (list) into a json file
    crawled_links_hash_object = json.dumps(get_crawled_links(crawled_pages)[1], indent=4)
    fileout = open("crawled-links-hash.json", "w")
    fileout.write(crawled_links_hash_object)
    fileout.close()

    # set the var crawled_links_hash
    filein = open("crawled-links-list.json", "r")
    crawled_links_hash = json.load(filein)
    filein.close()


    # save all words into a json file
    all_words_object = json.dumps(get_all_words(crawled_pages), indent=4)
    fileout = open("all-words.json", "w")
    fileout.write(all_words_object)
    fileout.close()

    filein = open("all-words.json", "r")
    all_words = json.load(filein) #(need updated) I don't need to load all of the words
    filein.close()


    # save crawled words into a json file
    crawled_words_object = json.dumps(get_crawled_words(all_words), indent=4)
    fileout = open("crawled-words.json", "w")
    fileout.write(crawled_words_object)
    fileout.close()

    filein = open("crawled-words.json", "r")
    crawled_words = json.load(filein)
    filein.close()

    int_links = map_int_link(crawled_links_list)

    # save the if-connect data into a json files
    urls_if_connect_object = json.dumps(get_url1_url2_connect(crawled_links_list, crawled_links_hash, crawled_pages), indent=4)
    fileout = open("urls-if-connect.json", "w")
    fileout.write(urls_if_connect_object)

    filein = open("urls-if-connect.json", "r")
    urls_if_connect = json.load(filein)
    filein.close()


    # 3. calculate pageranks and save them into a json file
    pageranks_object = json.dumps(calculate_page_ranks(crawled_links_list, crawled_pages, int_links, urls_if_connect), indent=4)

    # save the pageranks into a json file
    fileout = open("pageranks.json", "w")
    fileout.write(pageranks_object)
    fileout.close()

    # 4. calculate idfs for each crawled word and save them into a json file
    word_idf_object = json.dumps(calculate_idfs(crawled_pages, crawled_words, all_words), indent=4)
    fileout = open("word-idf.json", "w")
    fileout.write(word_idf_object)
    fileout.close()

    # 5. calculate tfs for each crawled word and save them into a json file
    word_tf_object = json.dumps(calculate_tfs(crawled_pages, crawled_words, all_words), indent=4)
    fileout = open("word-tf.json", "w")
    fileout.write(word_tf_object)
    fileout.close()


    # 4. return the number of total pages found during the crawl
    return len(already_crawled_list)
