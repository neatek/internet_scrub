# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class BookItem(scrapy.Item):
    name = scrapy.Field()
    authors = scrapy.Field()
    fullprice = scrapy.Field()
    price = scrapy.Field()
    link = scrapy.Field()
    rating = scrapy.Field()
    photos = scrapy.Field()
