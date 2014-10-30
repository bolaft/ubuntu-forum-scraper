#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Name:
spider.py

:Authors:
Soufian Salim (soufi@nsal.im)

:Date:
October 28th, 2014

:Description:
forum.ubuntu-fr.org forum spider
"""

from datetime import date
from scrapy import Spider, Selector, Item, Field
from settings import delay, start_date, end_date, thread_json_file
from time import sleep
from utility import make_url, extract_identifier, compute_date

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
			start_urls.append(thread["url"])


	def parse(self, response):
		"""
		Parses the http://forum.ubuntu-fr.org thread pages
		"""
		sleep(delay)

		for bp in response.css(".blockpost"):
			bp_selector = Selector(text=bp.extract())

			post = Post(
				author=bp_selector.xpath("//strong/text()").extract()[0],
				number=int(bp_selector.xpath("//h2/span/span/text()").extract()[0][1:]),
				datetime=str(compute_date(bp_selector.xpath("//h2/span/a/text()").extract()[0])),
				content=bp_selector.css(".postmsg").extract()[0].replace("<div class=\"postmsg\">\n\t\t\t\t\t\t<p>", "")[:-6],
				thread=extract_identifier(response.request.url)
			)

			yield post