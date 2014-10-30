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
from settings import delay, start_date, end_date, forum_json_file
from time import sleep
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


class ThreadSpider(Spider):
	"""
	This spider crawls forum.ubuntu-fr.org forums to scrape thread information
	"""
	name = "thread"

	allowed_domains = ["forum.ubuntu-fr.org"]

	start_urls = []

	with codecs.open(forum_json_file, "r", "utf-8") as json_data:
		json_forums = json.load(json_data)

		for forum in json_forums:
			start_urls.append(forum["url"])


	def parse(self, response):
		"""
		Parses the http://forum.ubuntu-fr.org forum pages
		"""
		sleep(delay)

		table_selector = Selector(text=response.css(".blocktable").extract()[0])

		for tr in table_selector.xpath("//tbody/tr"):
			tr_selector = Selector(text=tr.extract())
			link = tr_selector.xpath("//a/@href").extract()[0]

			thread = Thread(
				identifier=extract_identifier(link),
				name=tr_selector.xpath("//a/text()").extract()[0],
				url=make_url(link),
				sticky=True if "sticky" in tr_selector.extract() else False,
				closed=True if "closed" in tr_selector.extract() else False,
				forum=extract_identifier(response.request.url)
			)

			yield thread