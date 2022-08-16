import scrapy
from urllib.parse import unquote, urlparse, urlsplit
from pathlib import PurePosixPath
from bs4 import BeautifulSoup
import os

class RedditSpider(scrapy.Spider):
    name = 'reddit'
    allowed_domains = ['old.reddit.com', ]
    start_urls = ['https://old.reddit.com/r/retardedcornfieldcum']

    def parse(self, response):
        url1 = response.url
        print('Crawing url:', url1)
        html_path = urlparse(url1).path
        file_path = "subreddit/spiders/html" + html_path
        if file_path.endswith('/'):
            os.makedirs(file_path, exist_ok=True)
            file_path = file_path + "index.html"
        html_file = open(file_path, 'w')
        html_file.write(response.body.decode('utf-8'))
        html_file.close()
        bs = BeautifulSoup(response.body, 'html.parser')
        tag = bs.find_all('a')
        for a in tag:
            if a.has_attr('href'):
                if 'r/retardedcornfieldcum' in a['href']:
                    complete_url_next_page = response.urljoin(a['href'])
                    complete_url_next_page = urlsplit(complete_url_next_page)._replace(query=None).geturl()
                    yield scrapy.Request(url=complete_url_next_page, callback=self.parse)
