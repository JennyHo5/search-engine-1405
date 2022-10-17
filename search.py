# phrase:  A string representing a phrase searched by a user. This string may contain multiple words, separated by spaces
# boost: A boolean value representing whether the content score for each page should be boosted by that page's PageRank value (True) or not (False). If the boost value is True, the content score (i.e., cosine similarity score) for a page must be multiplied by the page's PageRank value to determine the page’s overall search score for the query.

# This function must perform the necessary search calculations to produce ranked results using the VECTOR SPACE MODEL and COSINE SIMILARITY APPROACH (see associated recording for details).

import searchdata
import math

# create a document vector for each document
    # 1. all words crawled has a specific integer
    # 2. the integer is the index in the vector
    # 3. each vector for a page = tf-idf

# turn the phrase (string) into a query
# only consider terms that have idf > 0
def get_search_query(phrase):
    query = phrase.split()
    search_query = []
    for word in query:
        if searchdata.get_idf(word) > 0:
            search_query.append(word)
    return search_query


def get_doc_vector(URL, phrase):
    doc_vector = []
    query = get_search_query(phrase)
    # calculate tf-idf for the doc with each word, add url:tf-idf to the vector
    for word in query:
        doc_vector.append(searchdata.get_tf_idf(URL, word))
    return doc_vector

# user's query is also represented as a document (a much shorter document)
# calculate tf-idf for the doc with each word, add url:tf-idf to the vector
def get_que_vector(phrase):
    que_vector = []
    query = get_search_query(phrase)

    # 1. for each word, first calculate the tf (occurences of word in query/total num of word in query)
    def get_que_tf(query, word):
        count = 0
        for i in query:
            if i == word:
                count += 1
        numerator = count
        denominator = len(query)
        tf = numerator / denominator
        return tf

    # 2. then calculate the idf (use the get_idf function from searchdata.py)

    # 3. return a query vector
    for word in query:
        tf = get_que_tf(query, word)
        idf = searchdata.get_idf(word)
        tf_idf = math.log(1 + tf) * idf
        que_vector.append(tf_idf)

    return que_vector

# get all the crawled urls
urls = searchdata.get_crawled_links()


def search(phrase, boost):
    # The function must return A LIST OF THE TOP 10 RANKED SEARCH RESULTS, SORTED FROM HIGHEST SCORE TO LOWEST. Each entry in this list must be a DICTIONARY with the following keys and associated values:
    # 1. url - The URL of the page
    # 2. title - The title of the page
    # 3. score – The total search score for the page

    result = []
    sorted_result = []

    # 1. get the query vector
    que_vector = get_que_vector(phrase)


    # 2. measure the left_denom (sqrt(query_vector_1^2 + query_vector_2^2 + ...))
    q_sum = 0
    for i in que_vector:
        q_sum += i * i
    left_denom = math.sqrt(q_sum)


    # 3. for each document(page), measure the similarity
    for URL in urls:

        # 3.0 sort the data using a dict
        page = {} # data of the page, including url, title, score
        page_title = searchdata.get_title(URL)
        page["url"] = URL
        page["title"] = page_title

        # 3.1 get the document vector for each document
        doc_vector = get_doc_vector(URL, phrase)
        # 3.2 measure the similarity between the query vector and the document vectors
        numerator = 0
        for i in range(len(que_vector)):
            numerator += que_vector[i] * doc_vector[i]


        # 3.3 measure the right_denom (sqrt(doc_vector_1^2 + doc_vector_2^2 + ...))
        d_sum = 0
        for i in doc_vector:
            d_sum += i * i
        right_denom = math.sqrt(d_sum)

        # only consider terms that exit in the query vector, if the page doesn't contain any word in the query, remove that URL from urls
        if right_denom == 0:
            continue

        cosine = numerator/(left_denom * right_denom)
        page["score"] = cosine
        result.append(page)

    # 4. if boost = True, boost by PageRank value
    if boost == True:
        for page in result:
            URL = page["url"]
            score = page["score"]
            pagerank = searchdata.get_page_rank(URL)
            page["score"] = pagerank * score

    # create a dict that key -> score, value -> original result, this is for sorting the result
    score_result = {}
    for page in result:
        score = page["score"]
        score_result[score] = page

    # 5.sort the result from the toppest to lowest
    for score, result in sorted(score_result.items()):
        sorted_result.append(result)

    return sorted_result
