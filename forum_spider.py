#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Name:
forum_spider.py

:Authors:
Soufian Salim (soufi@nsal.im)

:Date:
October 28th, 2014

:Description:
forum.ubuntu-fr.org forum spider
"""

from scrapy import Spider, Selector, Item, Field
from settings import excluded_categories
from utility import make_url, extract_identifier


class Forum(Item):
	"""
	Forum
	"""
	identifier = Field()
	name = Field()
	url = Field()
	category = Field()
	description = Field()
	parent = Field()


class ForumSpider(Spider):
	"""
	This spider crawls forum.ubuntu-fr.org looking to build forums maps containing threads, posts and related metadata
	"""
	name = "forum"

	allowed_domains = ["forum.ubuntu-fr.org"]

	start_urls = ["http://forum.ubuntu-fr.org"]

	def parse(self, response):
		"""
		Parses the http://forum.ubuntu-fr.org page for forums
		"""
		for bt in response.css(".blocktable"):
			bt_selector = Selector(text=bt.extract())

			category = bt_selector.xpath("//h2/span/text()").extract()[0]

			if category in excluded_categories:
				continue

			for tr in bt_selector.xpath("//tbody/tr"):
				tr_selector = Selector(text=tr.extract())

				description = tr_selector.css(".forumdesc").xpath("text()").extract()
				link = tr_selector.xpath("//a/@href").extract()[0]
				identifier = extract_identifier(link)

				forum = Forum(
					identifier=identifier,
					name=tr_selector.xpath("//h3/a/text()").extract()[0],
					url=make_url(link),
					category=category,
					description=description[0] if len(description) > 0 else None,
					parent=None
				)

				subforum_names = tr_selector.xpath("//div/a/text()").extract() + tr_selector.xpath("//div/a/strong/text()").extract()
				subforum_links = tr_selector.xpath("//div/a/@href").extract()

				subforums = [Forum(
					identifier=extract_identifier(link),
					name=name,
					url=make_url(link),
					category=category,
					description=None,
					parent=identifier
				) for name, link in zip(subforum_names, subforum_links)]

				forums = [forum] + subforums

				for forum in forums:
					yield forum