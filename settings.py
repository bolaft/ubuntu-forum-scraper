#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Name:
    settings.py

:Authors:
    Soufian Salim (soufi@nsal.im)
"""


from datetime import date


delay = 1

excluded_categories = [u"Activités autour du libre", u"Divers"]

start_date = date(2014, 9, 1)
end_date = date(2014, 9, 30)

forum_json_file = "data/forums.json"
thread_json_file = "data/threads.json"