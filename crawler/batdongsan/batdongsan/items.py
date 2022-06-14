# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class BatdongsanVnItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = Field()
    title = Field()
    postedTime = Field()
    description = Field()

    type = Field()
    square = Field()
    price = Field()
    legally = Field()

    address = Field()
    city = Field()
    district = Field()

    numOfBedrooms = Field()  # optional
    numOfToilets = Field()  # optional
    numOfFloors = Field()  # optional
    direction = Field()  # optional
    balconyDirection = Field()  # optional

    seller = Field()
    email = Field()
    phone = Field()
    image = Field()
