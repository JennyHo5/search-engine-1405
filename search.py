# phrase:  A string representing a phrase searched by a user. This string may contain multiple words, separated by spaces
# boost: A boolean value representing whether the content score for each page should be boosted by that page's PageRank value (True) or not (False). If the boost value is True, the content score (i.e., cosine similarity score) for a page must be multiplied by the page's PageRank value to determine the page’s overall search score for the query.

# This function must perform the necessary search calculations to produce ranked results using the VECTOR SPACE MODEL and COSINE SIMILARITY APPROACH (see associated recording for details). The function must return A LIST OF THE TOP 10 RANKED SEARCH RESULTS, SORTED FROM HIGHEST SCORE TO LOWEST. Each entry in this list must be a DICTIONARY with the following keys and associated values:
# 1. url - The URL of the page
# 2. title - The title of the page
# 3. score – The total search score for the page

# list = [
# {
# url: ...
# title: ...
# score: ...
# }
# ]

import searchdata

# create a document vector for each document
    # 1. all words crawled has a specific integer
    # 2. the integer is the index in the vector
    # 3. each vector for a page = tf-idf
def get_doc_vector(URL):
    doc_vector = []
    crawled_words = searchdata.get_crawled_words()
    # calculate tf-idf for the doc with each word, add url:tf-idf to the vector
    for word in crawled_words:
        doc_vector.append(searchdata.get_tf_idf(URL, word))
    return doc_vector



def search(phrase, boost):
    # 1. turn the phrase (string) into a query vector
    queue = phrase.split()
    return queue


    # 2. measure the similarity between the query vector and the document vector
    # 3. if boost = True, boost by PageRank value
