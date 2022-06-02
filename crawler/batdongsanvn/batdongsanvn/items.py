# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from itemloaders.processors import Identity


class BatdongsanvnItem(Item):
    title = Field()  # Ok
    address = Field()  # Ok
    city = Field()
    ward = Field()  # Ok
    district = Field()  # Ok
    square = Field()  # Ok
    type = Field()  # Ok
    price = Field()  # Ok
    description = Field()  # Ok
    seller = Field()  # Ok
    email = Field()
    phone = Field()
    time = Field()
    link = Field()
    image = Field(output_processor=Identity())
