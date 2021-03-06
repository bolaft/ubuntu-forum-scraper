#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Name:
assembler.py

:Authors:
Soufian Salim (soufi@nsal.im)

:Date:
October 30th, 2014

:Description:
Assembles data collected by the forum, thread and post spiders
"""

from optparse import OptionParser
from progressbar import ProgressBar
from settings import forum_json_file, thread_json_file, post_json_file

import codecs
import json
import io


def assemble(options, output_file):
    """
    Assembles and exports forum, thread and post data
    """

    n_threads = 0
    n_posts = 0

    with codecs.open(options.forum_file, "r", "utf-8") as json_forum_data:
        json_forums = json.load(json_forum_data)

        with codecs.open(options.thread_file, "r", "utf-8") as json_thread_data:
            json_threads = json.load(json_thread_data)

            with codecs.open(options.post_file, "r", "utf-8") as json_post_data:
                json_posts = json.load(json_post_data)

                posts_by_thread_id = {}
                thread_ids = []

                for post in json_posts:
                    if post["thread"] not in posts_by_thread_id:
                        posts_by_thread_id[post["thread"]] = []
                    posts_by_thread_id[post["thread"]].append(post)
                    if post["thread"] not in thread_ids:
                        thread_ids.append(post["thread"])

                threads_by_forum_id = {}
                forum_ids = []
                threads_by_id = {}

                for thread in json_threads:
                    threads_by_id[thread["identifier"]] = thread
                    if thread["forum"] not in threads_by_forum_id:
                        threads_by_forum_id[thread["forum"]] = []
                    threads_by_forum_id[thread["forum"]].append(thread)
                    if thread["forum"] not in forum_ids:
                        forum_ids.append(thread["forum"])

                forums_by_id = {}
                for forum in json_forums:
                    forums_by_id[forum["identifier"]] = forum

                progress = ProgressBar()

                for forum in progress(json_forums):
                    if forum["identifier"] not in forum_ids:
                        continue

                    forum["threads"] = []

                    if forum["identifier"] not in threads_by_forum_id:
                        continue

                    for thread in threads_by_forum_id[forum["identifier"]]:
                        thread["posts"] = []

                        if thread["identifier"] not in posts_by_thread_id:
                            continue

                        for post in posts_by_thread_id[thread["identifier"]]:
                            thread["posts"].append(post)

                        forum["threads"].append(thread)

                for forum in json_forums:
                    # empty threads (due to indesirable first and last post dates) are removed
                    to_be_removed = []

                    for thread in forum["threads"]:
                        del thread["forum"]

                        if len(thread["posts"]) == 0:
                            to_be_removed.append(thread)

                        for post in thread["posts"]:
                            if "thread" in post:
                                del post["thread"]

                        n_posts += len(thread["posts"])

                    for thread in to_be_removed:
                        forum["threads"].remove(thread)

                    n_threads += len(forum["threads"])

        with io.open(output_file, "w", encoding="utf-8") as f:
            f.write(unicode(json.dumps(json_forums, ensure_ascii=False)))

        print("Assembled map exported to " + output_file)
        print("{0} forums, {1} threads and {2} posts scraped".format(len(json_forums), n_threads, n_posts))


def parse_args():
    """
    Parse command line opts and arguments
    """

    op = OptionParser(usage="usage: %prog [opts]")

    op.add_option("--forum_file",
        dest="forum_file",
        default=forum_json_file,
        type="string",
        help="path to the json forum file")

    op.add_option("--thread_file",
        dest="thread_file",
        default=thread_json_file,
        type="string",
        help="path to the json thread file")

    op.add_option("--post_file",
        dest="post_file",
        default=post_json_file,
        type="string",
        help="path to the json post file")

    return op.parse_args()


if __name__ == "__main__":
    options, arguments = parse_args()

    assemble(options, arguments[0])
