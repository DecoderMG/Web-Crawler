from collections import deque
import urllib.request
import urllib.parse

index = {}
current_page = ''
base_urls = []

# TODO: Make the crawler polite by adhearing to robot.txt and scanning sitemaps.
# TODO: Finish page ranking algorithms
# TODO: Add sanitization for links

# Gets page content from URL to parse through
# Input: Url to a webpage (String)
# Output: if page loads:    Decoded webpage HTML (String)
#         else:             returns empty string (String)
def get_page(url):
    try:
        with urllib.request.urlopen(url) as response:
            return response.read().decode('utf-8')
    except:
        return ""

# Finds the next formatted link in current page
# and returns that link
# Inputs: Page
# Output: Next Link (String), Ending position of link (int)
def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
	url = page[start_quote + 1: end_quote]
    #url = sanitize_url(page[start_quote + 1:end_quote])
    return url, end_quote


#def sanitize_url(url):
#   sanitized_link = url
#    if '?' in url:
#        sanitized_link = url.rsplit('?', 1)[0]
#    return sanitized_link

def union(p, q):
    for e in q:
        if e not in p:
            p.append(e)


def get_all_links(page):
    links = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links


def crawl_web(seed):
    # Want to use deque for performance. deque.popleft has a runtime of O(1)
    # If we used .pop() from a list a shift is required thus runtime of O(n)
    # With many removals between tocrawled and crawled deque is a must at scale
    tocrawl = deque([seed])
    crawled = deque()
    graph = {}
    while tocrawl:
        page = tocrawl.popleft()
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index, page, content)
            outlinks = get_all_links(content)
            graph[page] = outlinks
            union(tocrawl, outlinks)
            crawled.append([page])
        print(tocrawl)
    return index, graph


# If the link exists in the index (dictionary) add to keyword

# If the keyword is not in the index,
# add an entry to the index

def add_to_index(index, keyword, url):
    if keyword in index:
        index[keyword].append(url)
    else:
        # not found, add new keyword to index (dictionary)
        index[keyword] = [url]


# Update the index to include
# all of the word occurences found in the
# page content by adding the url to the
# word's associated url list.

def add_page_to_index(index, url, content):
    keyword_list = content.split()
    for entry in keyword_list:
        add_to_index(index, entry, url)


# Return a dictionary object for the link
# of the urls associated
# with the keyword. If the keyword
# is not in the index, the procedure
# should return None.

def lookup(index, keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None


def lookup_best_result(index, keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None


# D-rank system to ensure high value pages are returned first
# This ranks pages based off number of quality links coming into the page.
#
def compute_ranks(graph):
    d = 0.8  # damping factor
    numloops = 10
    ranks = {}
    npages = len(graph)

    for page in graph:
        ranks[page] = 1.0 / npages

    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages

            for link in graph:
                if page in graph[link]:
                    newrank = newrank + d * ranks[link] / (len(graph[link]))

            newranks[page] = newrank
        ranks = newranks
    return ranks

#crawl_web('https://dreams.build')
