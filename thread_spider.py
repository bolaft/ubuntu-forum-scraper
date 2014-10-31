#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Name:
thread_spider.py

:Authors:
Soufian Salim (soufi@nsal.im)

:Date:
October 28th, 2014

:Description:
forum.ubuntu-fr.org thread spider
"""

from scrapy import Spider, Selector, Item, Field, Request
from settings import start_date, forum_json_file
from utility import make_url, extract_identifier, compute_date

import codecs, json


class Thread(Item):
	"""
	Thread
	"""
	identifier = Field()
	name = Field()
	url = Field()
	sticky = Field()
	closed = Field()
	forum = Field()
	last_post_date = Field()


class ThreadSpider(Spider):
	"""
	This spider crawls forum.ubuntu-fr.org forums to scrape thread information
	"""
	name = "thread"

	allowed_domains = ["forum.ubuntu-fr.org"]

	start_urls = []

	max_page = -1

	with codecs.open(forum_json_file, "r", "utf-8") as json_data:
		json_forums = json.load(json_data)

		for forum in json_forums:
			start_urls.append(forum["url"])


	def parse(self, response):
		"""
		Parses the http://forum.ubuntu-fr.org forum pages
		"""
		link_selector = Selector(text=response.css(".pagelink").extract()[0])
		links = link_selector.xpath("//a/text()").extract()

		page_count = int(links[-2]) if len(links) > 0 else 1

		for page_number in xrange(1, page_count + 1):
			yield Request("{0}&p={1}".format(response.request.url, page_number), callback=self.parse_page)


	def parse_page(self, response):
		"""
		Parses one page of the forum
		"""
		table_selector = Selector(text=response.css(".blocktable").extract()[0])

		for tr in table_selector.xpath("//tbody/tr"):
			tr_selector = Selector(text=tr.extract())
			link = tr_selector.xpath("//a/@href").extract()[0]
			date = tr_selector.xpath("//a/text()").extract()[-1]

			thread = Thread(
				identifier=extract_identifier(link),
				name=tr_selector.xpath("//a/text()").extract()[0],
				url=make_url(link),
				sticky=True if "sticky" in tr_selector.extract() else False,
				closed=True if "closed" in tr_selector.extract() else False,
				forum=extract_identifier(response.request.url),
				last_post_date=compute_date(date)
			)

			response.meta()

			if thread["last_post_date"] < start_date:
				break

			yield thread