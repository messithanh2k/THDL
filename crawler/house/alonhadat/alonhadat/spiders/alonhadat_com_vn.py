import scrapy
import logging
from scrapy.loader import ItemLoader
from scrapy import Selector
from itemloaders.processors import TakeFirst
from alonhadat.items import AlonhadatComVnItem
from scrapy.http import HtmlResponse


class AlonhadatComVnSpider(scrapy.Spider):
    name = 'alonhadat_com_vn'
    allowed_domains = ['alonhadat.com.vn']
    start_urls = ['https://alonhadat.com.vn/can-ban-nha.htm']

    custom_settings = {
        'CLOSESPIDER_ITEMCOUNT': 300,
        'DOWNLOAD_DELAY': 1
    }

    custom_settings = {
        'ITEM_PIPELINES': {
            'alonhadat.pipelines.AlonhadatComVnPipeline': 300
        }
    }

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
        list_post = response.css("div .ct_title > a")
        # print(list_post)
        for post in list_post:
            url = 'https://alonhadat.com.vn/'+post.attrib['href']
            yield scrapy.Request(url=url, callback=self.parse_item)

        # For next page
        next_page = 'https://alonhadat.com.vn/' + \
            response.css('div.page > a.active + a').attrib['href']
        yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_item(self, response, **kwargs):

        item_loader = ItemLoader(item=AlonhadatComVnItem(), response=response)
        item_loader.default_output_processor = TakeFirst()
        # Item

        title = response.css("h1::text").get()
        # print(title)
        item_loader.add_value('title', title.strip())
        time = response.css('span.date::text').get()
        item_loader.add_value('postedTime', time)
        description = response.css('div.detail::text').get()
        # print(description)
        item_loader.add_value('description', description)

        price = response.css("span.price>span.value::text").get()
        # print(price)
        item_loader.add_value('price', price.strip())
        square = response.css("span.square>span.value::text").get()
        # print(square)
        item_loader.add_value('square', square.strip())

        address = response.css("div.address>span.value::text").get()
        # print(address)
        item_loader.add_value('address', address.strip())

        prarams = response.css('td').getall()
        # print(prarams)
        for i in range(len(prarams)):
            item = prarams[i]
            item = item.replace('<td>', '')
            item = item.replace('</td>', '')
            if (item == 'Hướng'):
                direction = prarams[i +
                                    1].replace('<td>', '').replace('</td>', '').strip()
                # print(direction)
                item_loader.add_value('direction', direction.strip())
            if (item == 'Phòng ăn'):
                dinningRoom = prarams[i +
                                      1].replace('<td>', '').replace('</td>', '').strip()
                item_loader.add_value(
                    'dinningRoom', dinningRoom.strip())
                # print(dinningRoom)
            if (item == 'Loại BDS'):
                type = prarams[i+1].replace('<td>',
                                            '').replace('</td>', '').strip()
                item_loader.add_value('type', type)
            if (item == 'Đường trước nhà'):
                houseRoad = prarams[i +
                                    1].replace('<td>', '').replace('</td>', '').strip()
                item_loader.add_value('houseRoad', houseRoad)
            if (item == 'Nhà bếp'):
                kitchen = prarams[i+1].replace('<td>',
                                               '').replace('</td>', '').strip()
                item_loader.add_value('kitchen', kitchen)
            if (item == 'Pháp lý'):
                legally = prarams[i+1].replace('<td>',
                                               '').replace('</td>', '').strip()
                item_loader.add_value('legally', legally)
            if (item == 'Sân thượng'):
                rooftop = prarams[i+1].replace('<td>',
                                               '').replace('</td>', '').strip()
                item_loader.add_value('rooftop', rooftop)
            if (item == 'Chiều ngang'):
                width = prarams[i+1].replace('<td>',
                                             '').replace('</td>', '').strip()
                item_loader.add_value('width', width)
            if (item == 'Chiều dài'):
                length = prarams[i+1].replace('<td>',
                                              '').replace('</td>', '').strip()
                item_loader.add_value('length', length)
            if (item == 'Số lầu'):
                numOfFloors = prarams[i +
                                      1].replace('<td>', '').replace('</td>', '').strip()
                item_loader.add_value('numOfFloors', numOfFloors)
            if (item == 'Chổ để xe hơi'):
                garage = prarams[i+1].replace('<td>',
                                              '').replace('</td>', '').strip()
                item_loader.add_value('garage', garage)
            if (item == 'Số phòng ngủ'):
                numOfBedrooms = prarams[i +
                                        1].replace('<td>', '').replace('</td>', '').strip()
                item_loader.add_value('width', numOfBedrooms)
            if (item == 'Chính chủ'):
                proprietor = prarams[i +
                                     1].replace('<td>', '').replace('</td>', '').strip()
                item_loader.add_value('proprietor', proprietor)

        author = response.css(
            'div.contact-info > div.content > div.name::text').get()
        item_loader.add_value('seller', author)
        email = 'UNKNOW'
        item_loader.add_value('email', email)
        phone = response.css(
            'div.contact-info > div.content > div.fone >a::text').get()
        item_loader.add_value('phone', phone)

        images = response.css(
            'div.image-list >span>img').xpath('@src').getall()
        # print(images)
        image = []
        for item in images:
            image.append('https://alonhadat.com.vn/' + item)
        item_loader.add_value('image', image)
        # print(image)

        item_loader.add_value('url', response.request.url)

        return item_loader.load_item()