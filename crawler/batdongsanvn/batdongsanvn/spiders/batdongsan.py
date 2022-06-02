import scrapy
import logging
from scrapy.loader import ItemLoader
from scrapy import Selector
from itemloaders.processors import TakeFirst
from batdongsanvn.items import BatdongsanvnItem


class BatdongsanSpider(scrapy.Spider):
    name = 'batdongsan'
    allowed_domains = ['batdongsan.vn']
    start_urls = ['https://batdongsan.vn/ban-dat']

    custom_settings = {
        'CLOSESPIDER_ITEMCOUNT': 1000,
        'DOWNLOAD_DELAY': 1
    }

    # custom_settings = {
    #     'ITEM_PIPELINES': {
    #         'batdongsan.pipelines.BatDongSanPipeline': 300
    #     }
    # }

    def start_requests(self):
        headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'DNT': '1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
            'Sec-Fetch-User': '?1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        for url in self.start_urls:
            yield scrapy.Request(url, headers=headers)

    def parse(self, response, **kwargs):
        list_post = response.css("div .item .image > a")
        # print(list_post)
        for post in list_post:
            url = post.attrib['href']
            yield scrapy.Request(url=url, callback=self.parse_item)

        # For next page

        next_page = response.xpath("//a[contains(@rel,'next')]/@href").get()
        yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_item(self, response, **kwargs):
        # print(response)
        item_loader = ItemLoader(item=BatdongsanvnItem(), response=response)

        item_loader.default_output_processor = TakeFirst()
        # Item
        title = response.css("h1>span::text").get()
        # print(title)
        item_loader.add_value('title', title)
        # Address
        address = response.xpath(
            '//*[@id="post-detail"]/body/div[6]/div/div/div/div[2]/div/div[1]/div/div/div/div/div/div[2]/ul/li[2]/text()').get()
        # print(address)
        item_loader.add_value('address', address)

        # City
        info_address = address.strip().split(',')
        city = info_address[-1].strip()
        # print(city)
        item_loader.add_value('city', city)
        # District
        district = info_address[-2].strip()
        # print(district)
        item_loader.add_value('district', district)
        # Ward
        ward = info_address[-3].strip()
        item_loader.add_value('ward', ward)
        # print(ward)
        # Price
        price = response.css("strong.price::text").get()
        # print(price)
        item_loader.add_value('price', price.strip())
        # Square
        square = response.xpath(
            '//*[@id="post-detail"]/body/div[6]/div/div/div/div[2]/div/div[1]/div/div/div/div/div/div[2]/ul/li[1]/text()').get()
        # print(square)

        item_loader.add_value('square', square.strip())
        # Link
        item_loader.add_value('link', response.request.url)
        # Description
        description = response.css(
            '.body .content ::text').getall()
        # print(description)
        item_loader.add_value('description', ' '.join(description))

        # Seller
        author = response.css(
            'div.header > div.name > a::text').get()
        # print(author)
        item_loader.add_value('seller', author.strip())

        email = response.css('div.more.email > a::text').get()
        # print(email)
        item_loader.add_value('email', email)

        phone = response.css('div.more.phone > a::text').get()
        # print(phone)
        item_loader.add_value('phone', phone.strip())

        # Time post

        time = response.css(
            'time.timeago').attrib['datetime']
        # print(time)
        item_loader.add_value('time', time.strip())

        return item_loader.load_item()
