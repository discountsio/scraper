# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    discount_percentage = scrapy.Field()
    prize_now = scrapy.Field()
    original_prize = scrapy.Field()
    emi = scrapy.Field()
    product_link = scrapy.Field()
    list_page_link = scrapy.Field()
    page = scrapy.Field()
