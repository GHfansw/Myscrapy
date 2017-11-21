#! python3
# -*- coding: utf-8 -*-
# @Time     : 上午9:20
# @Author   : melon


import scrapy
from bs4 import BeautifulSoup
'''
name: identifies the Spider. It must be unique within a project, 
      that is, you can’t set the same name for different Spiders.
start_requests(): must return an iterable of Requests (you can return a list of requests or write a generator function) 
                  which the Spider will begin to crawl from. Subsequent requests will be generated successively from 
                  these initial requests.
parse(): a method that will be called to handle the response downloaded for each of the requests made. 
         The response parameter is an instance of TextResponse that holds the page content and has further 
         helpful methods to handle it.

The parse(): method usually parses the response, extracting the scraped data as dicts and also finding new URLs 
             to follow and creating new requests (Request) from them.
'''
# get a single page, then save it as a html


class QuotesSpider(scrapy.Spider):
    name = 'zhihu'

    def start_requests(self):
        headers = {
            "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36',
            "Referer": "https://zhuanlan.zhihu.com/",
            'Host': 'zhuanlan.zhihu.com',
        }

        urls = [
            'https://zhuanlan.zhihu.com/p/25994070',  # artical page
            'https://zhuanlan.zhihu.com/api/recommendations/posts?limit=4&seed=30',  # recommendation page
        ]
        '''
        Instead of implementing a start_requests() method that generates scrapy.Request objects from URLs, 
        you can just define a start_urls class attribute with a list of URLs. 
        start_urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        '''
        for url in urls:
            yield scrapy.Request(url=url, headers=headers, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        title = soup.title.string
        filename = 'crawl-%s.html' % title
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
