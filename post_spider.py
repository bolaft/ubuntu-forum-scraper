#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Name:
post_spider.py

:Authors:
Soufian Salim (soufi@nsal.im)

:Date:
October 28th, 2014

:Description:
forum.ubuntu-fr.org post spider
"""

from scrapy import Spider, Selector, Item, Field, Request
from settings import start_date, end_date, thread_json_file
from utility import extract_identifier, compute_date

import codecs, json


class Post(Item):
	"""
	Post
	"""
	author = Field()
	thread = Field()
	number = Field()
	datetime = Field()
	content = Field()
	signature = Field()
	modification = Field()


class PostSpider(Spider):
	"""
	This spider crawls forum.ubuntu-fr.org threads to scrape post information
	"""
	name = "post"

	allowed_domains = ["forum.ubuntu-fr.org"]

	start_urls = []

	with codecs.open(thread_json_file, "r", "utf-8") as json_data:
		json_threads = json.load(json_data)

		for thread in json_threads:
			if thread["last_post_date"] < start_date:
				continue

			start_urls.append(thread["url"])


	def parse(self, response):
		"""
		Parses the http://forum.ubuntu-fr.org thread pages
		"""

		link_selector = Selector(text=response.css(".pagelink").extract()[0])
		links = link_selector.xpath("//a/text()").extract()

		page_count = int(links[-2]) if len(links) > 0 else 1

		bp_selector = Selector(text=response.css(".blockpost")[0].extract())
		first_post_date = compute_date(bp_selector.xpath("//h2/span/a/text()").extract()[0])

		if first_post_date > end_date:
			return

		for page_number in xrange(1, page_count + 1):
			yield Request("{0}&p={1}".format(response.request.url, page_number), callback=self.parse_page)


	def parse_page(self, response):

		"""
		Parses one page of the forum
		"""

		for bp in response.css(".blockpost"):
			bp_selector = Selector(text=bp.extract())

			message = "".join(bp_selector.xpath(
				"//div[@class='postmsg']/node()[not(local-name() = 'div' and @class='postsignature') and not(local-name() = 'p' and @class='postedit')]"
			).extract()).strip()

			signature = bp_selector.css(".postsignature").xpath("p/node()").extract()

			modification = bp_selector.css(".postedit").extract()

			if len(modification) > 0:
				s = modification[0]
				modification = str(compute_date(s[s.find("(")+1:s.find(")")]))
			else:
				modification = False

			post = Post(
				author=bp_selector.xpath("//strong/text()").extract()[0],
				number=int(bp_selector.xpath("//h2/span/span/text()").extract()[0][1:]),
				datetime=str(compute_date(bp_selector.xpath("//h2/span/a/text()").extract()[0])),
				content=message,
				signature="".join(signature).strip() if len(signature) > 0 else False,
				modification=modification,
				thread=extract_identifier(response.request.url)
			)

			yield post