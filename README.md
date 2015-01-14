ubuntu-forum-scraper
====================

Downloads portions of the online francophone Ubuntu forums at `forum.ubuntu-fr`.

Usage: `./run.sh`. The download delay (time between requests) is defined in the `run.sh` file. Other parameters such as the start and end dates, excluded forum categories as well as target .json files are defined in the `settings.py` file.

The program works as follows:

1. Deletes previous data files
2. Scrapes the main forum page for forum informations (excluding some categories) and exports them as a json file
3. For each forum, scrapes the list of threads and exports it as json file
4. For each thread, scrapes all posts (if at least one post in the thread is within the defined time span) and exports them as a json file
5. Combines all three json files into one, removing empty (undesirable) threads
