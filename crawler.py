# perform the web crawling

import webdev
import json
import os

def find_title(str):
    start_title_index = str.find("<title>")
    end_title_index = str.find("</title>")
    title = str[start_title_index + 7 : end_title_index]
    return title

def find_words(str):
    words = []
    while "<p>" in str:
        start_p_index = str.find("<p>")
        end_p_index = str.find("</p>")
        p = str[start_p_index + 3 : end_p_index].split()
        for i in p:
            words.append(i)
        # delete the saved p and find the next new p
        str = str[: start_p_index] + str[end_p_index + 5:]
    return words

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
        start_a_index = html.find('<a href="')
        end_a_index = html.find('</a>')
        a = html[start_a_index + 9 : end_a_index]
        for cha in a:
            end_quotation_index = a.find('">')
            link = a[: end_quotation_index]
            link = rel_or_abs(link, seed)
        links.append(link)
        html = html[: start_a_index] + html[end_a_index + 5:]
    return links


def crawl(seed):

    # 1. Reset any existing data
    # delete all files and information from previous crawl

    curr_dir = os.getcwd()
    cache_dir = curr_dir + "/__pycache__"

    # 1.1 delete all the json files in the current directory
    for filename in os.listdir(curr_dir):
        if filename.endswith("json"):
            os.remove(filename)

    # 1.2 clean cache (?)
    for file in os.listdir(cache_dir):
        os.remove(os.path.join(cache_dir, file))
    os.rmdir(cache_dir)

    # 2. perform a web crawl starting at seed URL
        # 2.1 create a list of URLs that we need to visit
    queue = []

    already_crawled = [] # a list to track the page that we've already crawled so that we can skip them
        # 2.2 add the inital URL to the queue
    queue.append(seed)

        # 2.3 repeat until the queue is empty
    while len(queue) != 0:

            # 2.3.1 get the next URL from the queue
        link = queue.pop(0)

        # if the page has alreadt crawled, skip it
        if link in already_crawled:
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
            queue.append(i)


        curr_data = json.dumps(curr_page, indent=4) # python dict -> JSON object

        json_name = title + ".json" # save that JSON object into a new file
        fileout = open(json_name, "w")
        fileout.write(curr_data)
        fileout.close()

        # add current page to the list "already_crawled"
        already_crawled.append(link)

            # 2.3.3 find and crawler other pages linked to those pages


        # 2.3 PARSE those pages (extract links, extract words)

        # 2.4 generate all data required
        # 2.5 save those data to files

    # 3. return the number of total pages found during the crawl
    return len(already_crawled)
