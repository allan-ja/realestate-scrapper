# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RealestateScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class AtlantiqueSudItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    built_area = scrapy.Field()
    lot_area = scrapy.Field()
    bedrooms = scrapy.Field()
    bathrooms = scrapy.Field()
    price = scrapy.Field()
    location = scrapy.Field()

