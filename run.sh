#!/bin/sh

rm data/*.json

scrapy runspider forum_spider.py -o data/forums.json -s DOWNLOAD_DELAY=4
scrapy runspider thread_spider.py -o data/threads.json -s DOWNLOAD_DELAY=4
scrapy runspider post_spider.py -o data/posts.json -s DOWNLOAD_DELAY=4

./assembler.py data/map.json