def get_page(url):
    try:
		import urllib
		return urllib.urlopen(url).read()
	except:
		return ""

def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1: 
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)

def get_all_links(page):
    links = []
    while True:
        url,endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links

def crawl_web(seed):
    tocrawl = [seed]
    crawled = []
	index = {}
    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled:
			content = get_page(page)
			add_page_to_index(index, page, content)
            union(tocrawl, get_all_links(get_page(page)))
            crawled.append(page)
    return index
	
	
# If the link exists in the index (dictionary) add to keyword

# If the keyword is not in the index,
# add an entry to the index

index = []

def add_to_index(index,keyword,url):
    if keyword in index:
		index[keyword].append(url)
    else:
        # not found, add new keyword to index (dictionary)
		index[keyword] = [url]
		
# Update the index to include
# all of the word occurences found in the
# page content by adding the url to the
# word's associated url list.

def add_page_to_index(index,url,content):
    keyword_list = content.split()
    for entry in keyword_list:
        add_to_index(index, entry, url)
		
# Return a dictionary object for the link
# of the urls associated
# with the keyword. If the keyword
# is not in the index, the procedure
# should return None.

def lookup(index,keyword):
	if keyword in index:
		return index[keyword]
	else:
		return None