#!/bin/sh

rm data/*.json

scrapy runspider forum_spider.py -o data/forums.json
scrapy runspider thread_spider.py -o data/threads.json
scrapy runspider post_spider.py -o data/posts.json