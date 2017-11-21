#! python3
# -*- coding: utf-8 -*-
# @Time     : 上午9:20
# @Author   : melon


from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from bs4 import BeautifulSoup

from myscrapytest.items import ZhihuItem


# get a zhuanlan page, then get all the articals
# 只爬取了个人主页的内容标题和url 当需要下拉执行ajax时并不能继续爬取
# 但是这个是会follow已经获取的链接中的其他符合rule的链接
class ZhihuSpider(CrawlSpider):
    name = 'zhihu2'
    allowed_domains = ['zhuanlan.zhihu.com']
    start_urls = [
        'https://zhuanlan.zhihu.com/bankk',
    ]
    rules = (
        Rule(LinkExtractor(allow=('https://zhuanlan.zhihu.com/(\w+)*$',)), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=('https://zhuanlan.zhihu.com/p/(\d+)*$',)), callback='parse_item', follow=True),
        Rule(LxmlLinkExtractor(allow=('/p/(\d+)*$',), tags=('a',), attrs=('href', ), process_value='add_links'), callback='parse_item', follow=True),
    )

# 这里使用了pipline来进行存储item的工作
# 当需要多使用不同的pipline时，删除setting中的pipline，在各个spider中自己定义pipline，或者在pipline中进行逻辑判断
    # custom_settings = {
    #     'ITEM_PIPELINES': {
    #         'myscrapytest.pipelines.ZhihuPipeline': 400
    #     }
    # }
    def parse_item(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        title = soup.title.string
        item = ZhihuItem()
        item['title'] = title
        item['url'] = response.url
        yield item
        # self.log('Saved file %s' % filename)

    def add_links(self, value):
        return 'https://zhuanlan.zhihu.com' + value

