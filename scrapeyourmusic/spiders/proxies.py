import re
from itertools import count, islice

from pyquery import PyQuery as pq

import scrapy
from scrapeyourmusic.items import Proxy
from scrapy.selector import Selector


class ProxySpider(scrapy.Spider):
    name = "proxy_scraper"
    allowed_domains = ["incloak.com"]
    start_urls = ['https://incloak.com/proxy-list/?type=s#list']

    def parse(self, response):
        for proxy in self.parse_proxy_list(response):
            yield proxy

        pq_response = pq(response.text)
        pagination = pq_response('.proxy__pagination') \
            .find('li') \
            .not_('.arrow__left,.arrow__right,.is-active') \
            .find('a')

        for page in pagination:
            print(page)
            pq_page = pq(page)
            print(pq_page.attr('href'))
            yield scrapy.Request('https://incloak.com' + pq_page.attr('href'),
                                 callback=self.parse_proxy_list)

    def parse_proxy_list(self, response):
        print('in parse_proxy_list')
        pq_proxies = pq(response.text)

        proxy_list = pq_proxies('table.proxy__t tbody tr')
        for proxy in proxy_list:
            item = Proxy()
            pq_proxy = pq(proxy)

            item['ip_address'] = pq_proxy('td.tdl').text()
            item['port'] = pq_proxy('td').eq(1).text()

            yield item
