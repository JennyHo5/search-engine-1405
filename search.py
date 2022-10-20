# phrase:  A string representing a phrase searched by a user. This string may contain multiple words, separated by spaces
# boost: A boolean value representing whether the content score for each page should be boosted by that page's PageRank value (True) or not (False). If the boost value is True, the content score (i.e., cosine similarity score) for a page must be multiplied by the page's PageRank value to determine the page’s overall search score for the query.

# This function must perform the necessary search calculations to produce ranked results using the VECTOR SPACE MODEL and COSINE SIMILARITY APPROACH (see associated recording for details).

import searchdata
import math
import json


# create a document vector for each document
    # 1. all words crawled has a specific integer
    # 2. the integer is the index in the vector
    # 3. each vector for a page = tf-idf

# turn the phrase (string) into a query
# number of unique words -> number of entries (tfidf) to the words
# only consider terms that exist in query vector and have idf > 0
def get_search_query(phrase): # phrase = 'coconut coconut orange blueberry lime lime lime tomato'
    query = phrase.split()
    query = list(dict.fromkeys(query)) # delete duplicate words # query = ['coconut', 'orange', 'blueberry', 'lime', 'tomato']
    search_query = []
    for word in query:
        if searchdata.get_idf(word) > 0:
            search_query.append(word)
    return search_query # query = ['coconut', 'orange', 'blueberry', 'lime']


def get_doc_vector(URL, query): # query = ['coconut', 'orange', 'blueberry', 'lime']
    doc_vector = [] # tf-idf for each words in query
    # calculate tf-idf for the doc with each word, add tf-idf to the vector
    for word in query:
        doc_vector.append(searchdata.get_tf_idf(URL, word))
    return doc_vector # [0.1, 0.2]

# for each word in the query, calculate the tf (occurences of word in the phrase/total num of word in the phrase)
def get_que_tf(phrase,  word):
    phrase = phrase.split() # phrase = 'coconut coconut orange blueberry lime lime lime tomato'
    count = phrase.count(word)
    numerator = count
    denominator = len(phrase)
    tf = numerator / denominator
    return tf


# user's query is also represented as a document (a much shorter document)
# calculate tf-idf for the doc with each word, add url:tf-idf to the vector
def get_que_vector(phrase, query):
    que_vector = []
    for word in query:
        tf = get_que_tf(phrase, word)
        idf = searchdata.get_idf(word) # idf for a word
        tf_idf = math.log(1 + tf, 2) * idf # if-idf for a word-document (in this case word-query)
        que_vector.append(tf_idf)
    return que_vector



# phrase, boost -> sorted_result
def search(phrase, boost):

    # get crawled pages from the json object crawled-pages.json
    filein = open("crawled-pages.json", "r")
    crawled_pages = json.load(filein)
    filein.close()

    # get crawled pages from the json object crawled-pages.json
    filein = open("crawled-links-list.json", "r")
    crawled_links_list = json.load(filein)
    filein.close()

    filein = open("crawled-words.json", "r")
    crawled_words = json.load(filein)
    filein.close()

    filein = open("all-words.json", "r")
    all_words = json.load(filein)
    filein.close()

    filein = open("crawled-pages.json", "r")
    crawled_pages = json.load(filein)
    filein.close()

    # The function must return A LIST OF THE TOP 10 RANKED SEARCH RESULTS, SORTED FROM HIGHEST SCORE TO LOWEST. Each entry in this list must be a DICTIONARY with the following keys and associated values:
    # 1. url - The URL of the page
    # 2. title - The title of the page
    # 3. score – The total search score for the page

    result = []

    # 0. turn the phrase user entered into a query
    query = get_search_query(phrase)

    # 1. get the query vector
    que_vector = get_que_vector(phrase, query)

    # 2. measure the left_denom (sqrt(query_vector_1^2 + query_vector_2^2 + ...))
    q_sum = 0
    for i in que_vector:
        q_sum += i * i
    left_denom = math.sqrt(q_sum)


    # 3. for each document(page), measure the similarity
    for URL in crawled_links_list:

        # 3.0 sort the data using a dict
        page = {} # data of the page, including url, title, score
        page_title = crawled_pages[URL]["title"]
        page["url"] = URL
        page["title"] = page_title


        # 3.1 get the document vector for each document
        doc_vector = get_doc_vector(URL, query)

        # 3.2 measure the numerator
        numerator = 0
        for i in range(len(que_vector)):
            numerator += que_vector[i] * doc_vector[i]


        # 3.3 measure the right_denom (sqrt(doc_vector_1^2 + doc_vector_2^2 + ...))
        d_sum = 0
        for i in doc_vector:
            d_sum += i * i
        right_denom = math.sqrt(d_sum)

        # 3.4 calculate the cosine of the page
        # if none of terms in the query vector exist in the page (right_denom == 0)
        if right_denom == 0:
            page["score"] = 0
        else:
            cosine = numerator/(left_denom * right_denom)
            page["score"] = cosine

        result.append(page) # the result

    # 4. if boost = True, boost by PageRank value
    if boost == True:
        for page in result:
            URL = page["url"]
            score = page["score"]
            pagerank = searchdata.get_page_rank(URL)
            page["score"] = pagerank * score


    # 5.sort the result from the toppest to lowest
    result = sorted(result, key = lambda x: x["score"], reverse = True)
    result = result[:10] # top 10

    return result
