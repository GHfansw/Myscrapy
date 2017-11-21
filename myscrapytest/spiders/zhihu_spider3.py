#! python3
# -*- coding: utf-8 -*-
# @Time     : 上午9:20
# @Author   : melon


import scrapy
import json
import re

# get a zhuanlan page, then get all the articals
# 获取所有的文章 直接通过发送ajax请求的方式
class ZhihuSpider(scrapy.Spider):
    name = 'zhihu3'
    allowed_domains = ['zhuanlan.zhihu.com']
    global headers
    global urls
    headers = {
        "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36',
        "Referer": "https://zhuanlan.zhihu.com/irinwind",
        'Host': 'zhuanlan.zhihu.com',
    }

    urls = [
        # 'https://zhuanlan.zhihu.com/api/columns/irinwind/posts?limit=20&offset=0',
        'https://zhuanlan.zhihu.com/api/columns/irinwind/posts?limit=1&offset=0',
    ]

    def start_requests(self):
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=headers)
    # https://zhuanlan.zhihu.com/api/columns/bankk/posts?limit=20&offset=0 选出专栏0-20的文章 然后页面Ajax进行显示
    # https://zhuanlan.zhihu.com/api/columns/irinwind/posts?limit=1&offset=0 只选出一个 然后re提取标题和url 存储
    def parse(self, response):
        with open('allartical2.txt', 'a') as f:
            title = re.findall(r'"title": "(.+?)"',response.text)
            url = re.findall(r'"url": "(.+?)"', response.text)
            t = title[0].encode('utf-8').decode('unicode-escape')
            u = url[0].encode('utf-8').decode('unicode-escape')
            f.write(t +"："+ u+'\n')
        if len(json.loads(response.text)) == 1:
            count = int(urls[-1].split("=")[-1])
            print(urls[-1].split("=")[0:-1])
            url = "=".join(urls[-1].split("=")[0:-1]) + '=' + str(count+1)
            urls.append(url)
            print(url)
            if len(urls) < 10:  # 只选九篇
                yield scrapy.Request(url=url, callback=self.parse, headers=headers)


        # soup = BeautifulSoup(response.text, 'lxml')
        # self.log('Saved file %s' % filename)


