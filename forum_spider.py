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

import io, json

from scrapy import Spider, Selector


class ForumSpider(Spider):
	name = "post_spider"

	allowed_domains = ["forum.ubuntu-fr.org"]

	start_urls = ["http://forum.ubuntu-fr.org"]

	def parse(self, response):
		forums = []

		for bt in response.css('.blocktable'):
			bt_selector = Selector(text=bt.extract())

			for tr in bt_selector.xpath("//tbody/tr"):
				tr_selector = Selector(text=tr.extract())

				description = tr_selector.css(".forumdesc").xpath("text()").extract()

				forums.append({
					"name": tr_selector.xpath("//h3/a/text()").extract()[0],
					"link": "forum.ubuntu-fr.org" + tr_selector.xpath("//a/@href").extract()[0],
					"category": bt_selector.xpath("//h2/span/text()").extract()[0],
					"description": description[0] if len(description) > 0 else None,
					"specializations": tr_selector.xpath("//div/a/strong/text()").extract(),
					"subforums": tr_selector.xpath("//div/a/text()").extract()
				})

		with io.open("forums.json", "w", encoding="utf-8") as out:
			out.write(unicode(json.dumps(forums, ensure_ascii=False)))