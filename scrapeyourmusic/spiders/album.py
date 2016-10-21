import re

from pyquery import PyQuery as pq

import scrapy
from scrapeyourmusic.items import Album
from scrapy.selector import Selector


class AlbumSpider(scrapy.Spider):
    name = "album_scraper"
    allowed_domains = ["rateyourmusic.com"]

    def start_requests(self):
        request = scrapy.Request(
            'https://rateyourmusic.com', callback=self.parse)
        request.meta['proxy'] = 'https://137.135.166.225:8130'
        yield [request]

    def parse(self, response):
        if response.status == 503:
            print(response.text)
        pq_resp = pq(response.text)
        album_anchors = pq_resp('a') \
            .filter(lambda i, this: str(pq(this).attr('href')).find('/release/') != -1) \
            .filter(lambda i, this: len(pq(this).children('img')) != 1)
        for album in album_anchors:
            album_href = pq(album).attr('href')
            request = scrapy.Request(
                'https://rateyourmusic.com' + album_href, callback=self.parse_album)
            request.meta['proxy'] = 'https://137.135.166.225:8130'
            yield request

    def parse_album(self, response):
        if response.status == 503:
            print(response.text)
        pq_body = pq(response.text)
        section_main_info = pq_body('.section_main_info')
        album_info = pq_body('table.album_info')

        item = Album()

        item['url'] = response.url
        item['name'] = section_main_info('.album_title').text()
        item['artist'] = album_info('.artist').text()
        item['type'] = album_info.find('th') \
            .filter(lambda i, this: pq(this).text() == 'Type') \
            .siblings('td').text()
        item['releaseDate'] = album_info.find('th') \
            .filter(lambda i, this: pq(this).text() == 'Released') \
            .siblings('td').text()
        item['releaseYear'] = album_info.find('th') \
            .filter(lambda i, this: pq(this).text() == 'Released') \
            .siblings('td').find('a b').text()

        item['recordedDate'] = album_info.find('th') \
            .filter(lambda i, this: pq(this).text() == 'Recorded') \
            .siblings('td').text()

        item['rating'] = album_info.find('th') \
            .filter(lambda i, this: pq(this).text() == 'RYM Rating') \
            .siblings('td').find('span span.avg_rating').text().strip()

        item['totalRatings'] = album_info.find('th') \
            .filter(lambda i, this: pq(this).text() == 'RYM Rating') \
            .siblings('td').find('span span.num_ratings b span').text().strip()

        item['rank'] = album_info.find('th') \
            .filter(lambda i, this: pq(this).text() == 'Ranked') \
            .siblings('td').find('b').text().strip()

        item['rankYear'] = album_info.find('th') \
            .filter(lambda i, this: pq(this).text() == 'Ranked') \
            .siblings('td').find('a').eq(0).text().strip()

        item['primaryGenres'] = album_info.find('th') \
            .filter(lambda i, this: pq(this).text() == 'Genres') \
            .siblings('td').find('div span.release_pri_genres a.genre') \
            .map(lambda i, this: pq(this).text())

        item['secondaryGenres'] = album_info.find('th') \
            .filter(lambda i, this: pq(this).text() == 'Genres') \
            .siblings('td').find('div span.release_sec_genres a.genre') \
            .map(lambda i, this: pq(this).text())

        item['language'] = album_info.find('th') \
            .filter(lambda i, this: pq(this).text() == 'Language') \
            .siblings('td').text()

        yield item
