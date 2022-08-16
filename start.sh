#!/usr/local/bin/zsh
source /datastore/rcc/venv/bin/activate
cd /datastore/rcc/subreddit
scrapy crawl reddit
cd subreddit/spiders/html
git add *
git add -u
date=date +%d.%m.%y
git commit -m "$date"
git push origin main
deactivate