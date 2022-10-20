# produce data required by search engine
# test the correctness of the data produced through crawler module
# read information from the json docs and produce correct outputs

import crawler
import webdev
import os
import json
import matmult
import math


# URL -> a list of other URLs that the page with the given URL links to
def get_outgoing_links(URL):
    filein = open("crawled-pages.json", "r")
    crawled_pages = json.load(filein)
    filein.close()
    filein = open("crawled-links-hash.json", "r")
    crawled_links_hash = json.load(filein)
    filein.close()
    # 1. if the URL was not found during the crawling process then return None
    if URL not in crawled_links_hash: # O(1)
        return None
    # 2. read the outgoing links of that url from cralwed-pages.json
    for key in crawled_pages:
        if key == URL:
            outgoing_links = crawled_pages[key]["links"]
    return outgoing_links

#URL - > a list of URLs for pages that link to the page with the given URL
def get_incoming_links(URL):
    filein = open("crawled-pages.json", "r")
    crawled_pages = json.load(filein)
    filein.close()
    filein = open("crawled-links-hash.json", "r")
    crawled_links_hash = json.load(filein)
    filein.close()
    # 1. if the URL was not found during the crawling process then return None
    if URL not in crawled_links_hash: # O(1)
        return None
    # 2. if the URL is in the list of the outgoing links of another URL, then include that another URL into the list
    incoming_links = []
    for page in crawled_pages:
        # if it is the same page, skip
        if URL == page:
            continue
        # if the links in the page include the current URL, store the page's link into incoming_links
        if URL in crawled_pages[page]["links"]:
            incoming_links.append(page)
    return incoming_links


# URL -> the PageRank value of the page with that URL
# what PageRank calculates: the probability the random surfer is on page x at any given time
def get_page_rank(URL):
    filein = open("pageranks.json", "r")
    pageranks = json.load(filein)
    filein.close()
    # 1. If the given URL was not found during the crawling process, this function must return the value -1
    if URL not in pageranks:
        return -1
    # 2. match the pagerank from the pagerank.json

    for key in pageranks:
        if key == URL:
            rank = pageranks[key]
    return rank

# Accepts a single string argument representing a word and returns the inverse document frequency of that word within the crawled pages
def get_idf(word):
    filein = open("word-idf.json", "r")
    words_idfs = json.load(filein)
    filein.close()

    # 1. if the word was not present in any crawled documents, this function must return 0
    if word not in words_idfs:
        return 0

    # 2. else, match the word with its idf
    for key in words_idfs:
        if word == key:
            return words_idfs[key]

# Accepts two string arguments: a URL and a word. This function must return the term frequency of that word within the page with the given URL
def get_tf(URL, word):
    filein = open("crawled-links-hash.json", "r")
    crawled_links_hash = json.load(filein)
    filein.close()

    # 1 if the URL does not found during the crawl, returin 0
    if URL not in crawled_links_hash:
        return 0

    # 2 else, match the url and the word with their tf
    filein = open("word-tf.json", "r")
    urls_words_tfs = json.load(filein)
    filein.close()
    for url in urls_words_tfs: # O(1)
        if url == URL:
            words_tfs = urls_words_tfs[url]
            if word not in words_tfs: # if word is not found in the page # O(1)
                return 0
            for i in words_tfs:
                if i == word:
                    return words_tfs[i]



# return the tf-idf weight for the given word within the page represented by the given URL
def get_tf_idf(URL, word):
    tf = get_tf(URL, word)
    idf = get_idf(word)
    tf_idf = math.log(1 + tf, 2) * idf
    return tf_idf
