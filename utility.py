#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Name:
    utility.py

:Authors:
    Soufian Salim (soufi@nsal.im)
"""

from datetime import datetime, timedelta


def make_url(link):
    """
    Makes a relative link absolute
    """
    base_url = "http://forum.ubuntu-fr.org/"
    return base_url + link.replace("./", "")


def extract_identifier(link):
    """
    Extracts item ids from links
    """
    if "&" in link:
        return int(link[link.index("id=") + 3:link.index("&")])
    else:
        return int(link[link.index("id=") + 3:])


def compute_date(s):
    """
    Extracts the date from the "dernier message" column cell in the thread table
    """
    if s.startswith("Aujourd'hui"):
        d = datetime.today()
    elif s.startswith("Hier"):
        d = datetime.today() - timedelta(days=1)
    else:
        ds = s[3:s.index(",")]
        d = datetime(int(ds[6:]), int(ds[3:5]), int(ds[0:2]))

    return d.replace(hour=int(s[-5:-3]), minute=int(s[-2:]), second=0, microsecond=0)