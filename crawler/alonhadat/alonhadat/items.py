# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy
from scrapy.item import Item, Field


class AlonhadatComVnItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = Field()
    title = Field()
    postedTime = Field()
    description = Field()
    type = Field()
    square = Field()
    price = Field()

    address = Field()
    city = Field()
    district = Field()

    houseRoad = Field()
    kitchen = Field()

    width = Field()
    length = Field()
    legally = Field()

    dinningRoom = Field()

    numOfFloors = Field()
    garage = Field()
    proprietor = Field()

    numOfBedrooms = Field()  # optional
    numOfToilets = Field()  # optional
    numOfFloors = Field()  # optional
    direction = Field()  # optional
    rooftop = Field()  # optional

    seller = Field()
    email = Field()
    phone = Field()
    image = Field()
