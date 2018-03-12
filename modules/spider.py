import argparse, os, sys, json, scrapy, logging, requests
from urlparse import urlparse
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


files = {}

class MySpider(scrapy.spiders.CrawlSpider):
	name = 'example.com'
	#allowed_domains = ['trelis24.github.io']
	start_urls = ['https://www.nicklevine.org/els2013']
	rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
		#Rule(LinkExtractor(allow=('/', ), deny=('subsection\.php', ))),
        # Extract links matching 'item.php' and parse them with the spider's method parse_item
		Rule(LinkExtractor(allow=('/', )), callback='parse_item'),
    )

	# Return a dictionary with files URLs
	def parse_item(self, response):
		global files
		file = open('file_extensions.txt')
		
		for href in response.xpath('//a/@href'):
			url2 = href.extract()
			#print url2
			url3 = urlparse(url2)
			if url3.scheme == "http" or url3.scheme == "https":
				print url2
				request = req.Request(url2)
				print request.text

				for ext in file:
					if url2.split('.')[-1] in ext:
						if ext in files: 
							files[ext].append(url2)
						else:
							files[ext] = [url2]
						break
		#print files

	def save_file(self, response):
		path = response.url.split('/')[-1]
		self.logger.info('Saving PDF %s', path)
		with open(path, 'wb') as f:
			f.write(response.body)


	def log(self,verbose):
		configure_logging(install_root_handler=verbose)
		logging.basicConfig(
			filename='/tmp/morsa.log',
			format='%(levelname)s: %(message)s',
			level=logging.INFO
		)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-host", help="https://host.com",required=True)
	parser.add_argument("-v", default=False, help="Verbose", action="store_true")
	args = parser.parse_args()

	spider = MySpider()
	spider.log(args.v)


	runner = CrawlerRunner()
	d = runner.crawl(MySpider)
	d.addBoth(lambda _: reactor.stop())
	reactor.run() # the script will block here until the crawling is finished




'''
TODO
https://docs.scrapy.org/en/latest/topics/spiders.html#scrapy.spiders.Spider

[] Blacklist
[] How deep
[] Hosts from file
[] Multi threading
'''

'''
INSTALLATION
pip install --upgrade scrapy
pip install --upgrade twisted
pip install --upgrade pyopenssl
'''