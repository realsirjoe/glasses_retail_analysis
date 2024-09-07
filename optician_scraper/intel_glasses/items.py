# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FielmannItem(scrapy.Item):
    name = scrapy.Field()
    product_id = scrapy.Field()
    color = scrapy.Field()
    images = scrapy.Field()
    brand = scrapy.Field()
    manufacturer = scrapy.Field()
    material = scrapy.Field()
    availability = scrapy.Field()
    currency = scrapy.Field()
    price = scrapy.Field()
    store = scrapy.Field()
    url = scrapy.Field()
    category = scrapy.Field()
    subcategory = scrapy.Field()
