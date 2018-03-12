import argparse, os, sys, json, logging, requests, Queue
from urlparse import urlparse
from lxml import html

# waiting, working, done, out_scope, files
queue = {'waiting':Queue.Queue(), 'working':[], 'done':[], 'out_scope':Queue.Queue(), 'files':Queue.Queue(), 'depth':0}

# Pre: host and a partial URL or path
# Post: full url (format: http(s)://host/path)
def parse_url(host,url):
	url = urlparse(url)	
	if url.scheme == '': # Relative paths -> host + rel.path
		if './' in url.path:
			url = url.path.split('/')[1:]
			url = '/'.join(url)
		else:
			url = url.path
		url = host + url
	else:
		url = url.scheme + '://' + url.netloc + url.path
	return url

# Pre: request
# Post: array with all URLs found in the body
def get_urls(r):
	body = html.fromstring(r.content)
	urls = body.xpath('//a/@href') # get links
	return urls

def add_to_queue(domain, url,r):
	global queue
	if url not in queue['done']:
		# In scope
		if domain in url:
			queue['waiting'].put(url)
		# Out of scope
		else:
			queue['out_scope'].put(url)

def crawl (host):
	global queue
	domain = host.split('//')[1]

	queue['working'].append(host)
	#print "Working: " + host
	if check_depth(host):
		r = requests.get(host)
		if check_if_file(r):
			queue['files'].put(host)
		else:
			urls = get_urls(r)
			for url in urls:
				url = parse_url(host,url)
				add_to_queue(domain,url,r)
	queue['working'].remove(host)
	queue['done'].append(host)
	#print "Done: " + host

# Pre: user depth and URL
# Post: -
def set_depth(d, url):
	depth = int(len(url.split('/'))) - 3 # -3 is because https://example.com/ has already 3 '/'
	queue['depth'] = depth + int(d)

# Pre: URL
# Post: return false if the url is deeper than the max depth 
def check_depth(url):
	global queue
	depth = len(url.split('/')) - 3 # -3 is because https://example.com/ has already 3 '/'
	if int(queue['depth']) > 0 and depth > int(queue['depth']):
		return False
	return True
	

# Pre: URL request
# Post: Return true if it is a file
def check_if_file(r):
	if 'content-type' in r.headers:
		if "text/html" in r.headers['content-type']: 
			return False
		else:
			return True
	return False

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-host", help="https://host.com/",required=True)
	parser.add_argument("-v", default=False, help="Verbose", action="store_true")
	parser.add_argument("-d", default=0, help="Depth")
	args = parser.parse_args()


	#queue['depth'] = args.host
	set_depth(args.d, args.host)
	#check_depth("http://example.com/hola/pse/")
	#crawl(args.host)

	crawl(args.host)
	while not queue['waiting'].empty():
		host = queue['waiting'].get()
		crawl(host)

	print queue
	while not queue['files'].empty():
		print queue['files'].get()


'''
TODO
https://docs.scrapy.org/en/latest/topics/spiders.html#scrapy.spiders.Spider

[] Blacklist
[x] How deep
[] Hosts from file
[] Multi threading
'''

'''
INSTALLATION
pip install --upgrade scrapy
pip install --upgrade twisted
pip install --upgrade pyopenssl
'''