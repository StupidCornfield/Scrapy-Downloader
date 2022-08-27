import scrapy
from urllib.parse import unquote, urlparse, urlsplit
from pathlib import PurePosixPath
from bs4 import BeautifulSoup
import os
import re
import copy
import sys

class RedditSpider(scrapy.Spider):
    name = 'reddit'
    allowed_domains = ['old.reddit.com', ]
    start_urls = ['https://old.reddit.com/r/retardedcornfieldcum']

    def parse(self, response):
        sys.setrecursionlimit(100000000)
        url1 = response.url
        print('Crawing url:', url1)
        if urlparse(url1).query is None or urlparse(url1).query is "":
            html_path = urlparse(url1).path
        else:
            html_path = urlparse(url1).path + "w" + urlparse(url1).query
            html_path = html_path.replace("=", "x")
            html_path = html_path.replace("&", "y")
        file_path = "subreddit/spiders/html" + html_path
        if file_path.endswith('/'):
            os.makedirs(file_path, exist_ok=True)
            file_path = file_path + "index.html"
        else:
            file_path = file_path + ".html"
        html_file = open(file_path, 'wb')
        body2 = response.body
        bs2 = BeautifulSoup(body2, 'html.parser')
        soup_new = copy.deepcopy(bs2)
        links = soup_new.find_all('a')
        for a in links:
            if a.has_attr('href'):
                if 'r/retardedcornfieldcum' in a['href']:
                    if 'old.reddit.com' in a['href']:
                        old_a = a
                        url2 = a['href']
                        url2 = url2.replace("old.reddit.com", "www.retardedcornfieldcum.com")
                        if "count" in url2:
                            url2 = re.sub("count=[0-9]+", "count=25", url2)
                        url2 = url2.replace("?", "w")
                        url2 = url2.replace("=", "x")
                        url2 = url2.replace("&", "y")
                        if not url2.endswith(".html"):
                            if not url2.endswith("/"):
                                url2 = url2 + ".html"
                        a['href'] = url2

        html_file.write(soup_new.prettify("utf-8"))
        html_file.close()
        print("Wrote file", file_path)
        bs = BeautifulSoup(response.body, 'html.parser')
        tag = bs.find_all('a')
        for a in tag:
            if a.has_attr('href'):
                if 'r/retardedcornfieldcum' in a['href']:
                    complete_url_next_page = response.urljoin(a['href'])
                    query = urlparse(complete_url_next_page).query
                    if "before" in query:
                        continue
                    if "sort" in query:
                        continue
                    if "count" in query:
                        if "count=25" in query:
                            yield scrapy.Request(url=complete_url_next_page, callback=self.parse)
                        else:
                            queryx = re.sub("count=[0-9]+", "count=25", query)
                            complete_url_next_page = urlsplit(complete_url_next_page)._replace(query=queryx).geturl()
                            yield scrapy.Request(url=complete_url_next_page, callback=self.parse)
                    else:
                        yield scrapy.Request(url=complete_url_next_page, callback=self.parse)
