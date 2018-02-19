import argparse, os, sys, json, scrapy
from scrapy.crawler import CrawlerProcess
verbose = 0


class MySpider(scrapy.spiders.CrawlSpider):
	name = 'example.com'
	allowed_domains = ['example.com']

	def start_requests(self):
		print "hi"
		yield scrapy.Request('http://www.example.com/1.html', self.parse)

	def parse(self, response):
		for h3 in response.xpath('//h3').extract():
			yield MyItem(title=h3)

		for url in response.xpath('//a/@href').extract():
			yield scrapy.Request(url, callback=self.parse)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-host", help="https://host.com",required=True)
	parser.add_argument("-v", help="Verbose",required=False, action='store_true')
	args = parser.parse_args()

	if args.v:
		verbose = 1

	process = CrawlerProcess({	})
	process.crawl(MySpider)
	process.start() # the script will block here until the crawling is finished

	
	print "hello world"



'''
TODO
https://docs.scrapy.org/en/latest/topics/spiders.html#scrapy.spiders.Spider

[] Blacklist
[] How deep
[] Hosts from file
[] Multi threading
'''