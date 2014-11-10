#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Name:
    settings.py

:Authors:
    Soufian Salim (soufi@nsal.im)
"""

from datetime import datetime

excluded_categories = [u"Activités autour du libre", u"Divers"]

start_date = datetime(2014, 10, 20)
end_date = datetime(2014, 10, 26)

forum_json_file = "data/forums.json"
thread_json_file = "data/threads.json"
post_json_file = "data/posts.json"