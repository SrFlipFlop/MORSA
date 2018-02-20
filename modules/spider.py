import argparse, os, sys, json, scrapy, logging
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class MySpider(scrapy.spiders.CrawlSpider):
	name = 'example.com'
	#allowed_domains = ['trelis24.github.io']
	start_urls = ['https://www.nicklevine.org/']
	rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
		#Rule(LinkExtractor(allow=('/', ), deny=('subsection\.php', ))),
        # Extract links matching 'item.php' and parse them with the spider's method parse_item
		Rule(LinkExtractor(allow=('/els2013', )), callback='parse_item'),
    )

	def parse_item(self, response):
		self.logger.info('Hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii, this is an item page! %s', response.url)
		for href in response.xpath('//a/@href'):
			print href.extract()


	def save_file(self, response):
		path = response.url.split('/')[-1]
		self.logger.info('Saving PDF %s', path)
		with open(path, 'wb') as f:
			f.write(response.body)

	# This method must return an iterable with the first Requests to crawl for this spider. It is called by Scrapy when the spider is opened for scraping. Scrapy calls it only once, so it is safe to implement start_requests() as a generator.
	'''def start_requests(self):
		logging.info("Start request")
		yield scrapy.Request('https://trelis24.github.io/', self.parse)

	# This is the default callback used by Scrapy to process downloaded responses, when their requests do not specify a callback.
	def parse(self, response):
		logging.info("Start parse")
		
		logging.info('A response from %s just arrived!', response.url)'''

	def log(self,verbose):
		configure_logging(install_root_handler=verbose)
		logging.basicConfig(
			filename='log.txt',
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