import math

doc1 = "apple apple peach peach apple peach apple"
doc2 = "apple apple apple apple apple apple apple"
doc3 = "banana peach banana banana banana peach peach peach peach peach peach"
doc4 = "banana banana banana"

docs = [doc1, doc2, doc3, doc4]

word = "apple"

# Accepts a single string argument representing a word and returns the inverse document frequency of that word within the crawled pages
def get_idf(word):
    # create a list that include all word crawled (no duplicate)
    crawled_words = ["apple", "banana", "peach"]

    # 1. if the word was not present in any crawled documents, this function must return 0
    if word not in crawled_words:
        return 0

    # 2. else, calculate frequency
        # 2.1 total document
    total_docs_num = len(docs)
        # 2.2 number of documents w appears in
    appear_num = 0
    for i in range(len(docs)):
        page_words = docs[i] # return a list of words on page
        if word in page_words:
            appear_num += 1
        # 2.3 calculate the frequency
    numerator = total_docs_num
    denominator = 1 + appear_num
    fraction = numerator / denominator
    idf = math.log(fraction, 2)
    return idf

print(get_idf(word))

# Accepts two string arguments: a URL and a word. This function must return the term frequency of that word within the page with the given URL
def get_tf(doc_num, word):
    # 1. If the word does not appear in the page with the given URL, or the URL has not been found during the crawl, this function must return 0
        # 1.1 if the URL does not found during the crawl, returin 0

        # 1.2 if the word does not appear in the page with the given URL, return 0
    curr_words = docs[doc_num].split()
    print(curr_words)
    if word not in curr_words:
        return 0

    # 2. claculate tf
        # 2.1 occurences of word in doc
    count = 0
    for i in curr_words:
        print(i)
        if i == word:
            count += 1
    numerator = count
    print(numerator)
    denominator = len(curr_words)
    tf = numerator / denominator
    return tf

doc_num = 0
print(get_tf(doc_num, word))

# return the tf-idf weight for the given word within the page represented by the given URL
def get_tf_idf(doc_num, word):
    tf = get_tf(doc_num, word)
    idf = get_idf(word)
    tf_idf = math.log(1 + tf, 2) * idf
    return tf_idf

print(get_tf_idf(doc_num, word))
