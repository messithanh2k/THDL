import scrapy
import logging
from scrapy.loader import ItemLoader
from scrapy import Selector
from itemloaders.processors import TakeFirst
from alomuabannhadat.items import AlomuabannhadatVnItem
from scrapy.http import HtmlResponse


class AlomuabannhadatVnSpider(scrapy.Spider):
    name = 'alomuabannhadat_vn'
    allowed_domains = ['alomuabannhadat.vn']
    start_urls = ['https://alomuabannhadat.vn/nha-ban-tai-ha-noi/',
                  'https://alomuabannhadat.vn/dat-ban-tai-ha-noi/']

    custom_settings = {
        'CLOSESPIDER_ITEMCOUNT': 300,
        'DOWNLOAD_DELAY': 1
    }

    custom_settings = {
        'ITEM_PIPELINES': {
            'alomuabannhadat.pipelines.AlomuabannhadatVnPipeline': 300
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
        list_post = response.css(
            "section#properties-search div.property div.info a")
        # print(list_post)
        for post in list_post:
            url = post.attrib['href']
            # print(url)
            yield scrapy.Request(url=url, callback=self.parse_item)

        # For next page
        next_page = response.css(
            'ul.pagination > li.active + li>a').attrib['href']
        yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_item(self, response, **kwargs):

        item_loader = ItemLoader(
            item=AlomuabannhadatVnItem(), response=response)
        item_loader.default_output_processor = TakeFirst()

        # Item

        title = response.css("h1::text").get()
        # print(title)
        item_loader.add_value('title', title.strip())

        # address = response.css("div.address>span.value::text").get()
        # # print(address)
        # item_loader.add_value('address', address.strip())

        price = response.css(
            "section#property-detail>header.property-title>figure b::text").getall()[1]
        # print(price)
        item_loader.add_value('price', price.strip())

        prarams = response.css('section#quick-summary>dl>dt').getall()
        values = response.css('section#quick-summary>dl>dd').getall()
        # print(prarams)
        # print(values)
        for i in range(len(prarams)):
            item = prarams[i]
            item = item.replace('<dt>', '')
            item = item.replace('</dt>', '')
            value = values[i].replace('<dd>', '').replace('</dd>', '')

            if (item == 'V??? tr??:'):
                location = value.strip()
                item_loader.add_value('location', location)

            if (item == 'Ph??p l??:'):
                legally = value.strip()
                item_loader.add_value('legally', legally)

            if (item == 'Li??n h???:'):
                author = value.strip()
                item_loader.add_value('seller', author)

            if (item == 'Ng??y ????ng:'):
                time = value.strip()
                # print(direction)
                item_loader.add_value('postedTime', time)
            if (item == 'Mobile:'):
                phone = value.split("')")[0].split("this,'")[1].strip()
                item_loader.add_value('phone', phone)

        params = response.css('section#property-features>ul>li::text').getall()

        for item in params:
            if (item.find('Di???n t??ch s??? d???ng:') >= 0):
                square = item.replace('Di???n t??ch s??? d???ng:', '')
                # print(square)
                item_loader.add_value('square', square)

            if (item.find('H?????ng x??y d???ng:') >= 0):
                direction = item.replace('H?????ng x??y d???ng:', '').strip()
                item_loader.add_value('direction', direction)

            if (item.find('Lo???i ?????a ???c:') >= 0):
                type = item.replace('Lo???i ?????a ???c:', '').strip()
                item_loader.add_value('type', type)

            if (item.find('???????ng tr?????c nh??:') >= 0):
                houseRoad = item.replace('???????ng tr?????c nh??:', '').strip()
                item_loader.add_value('houseRoad', houseRoad)

            if (item.find('S??? ph??ng kh??ch:') >= 0):
                numOfLivingrooms = item.replace('S??? ph??ng kh??ch:', '').strip()
                item_loader.add_value('numOfLivingrooms', numOfLivingrooms)

            if (item.lower().find('nh?? b???p') >= 0):
                kitchen = 1
                item_loader.add_value('kitchen', kitchen)

            if (item.lower().find('ph??ng ??n') >= 0):
                dinningRoom = 1
                item_loader.add_value('dinningRoom', dinningRoom)

            if (item.lower().find('s??n th?????ng') >= 0):
                rooftop = 1
                item_loader.add_value('rooftop', rooftop)

            if (item.find('Chi???u ngang:') >= 0):
                width = item.replace('Chi???u ngang:', '').strip()
                item_loader.add_value('width', width)

            if (item.find('Chi???u d??i:') >= 0):
                length = item.replace('Chi???u d??i:', '').strip()
                item_loader.add_value('length', length)

            if (item.find('S??? l???u:') >= 0):
                numOfFloors = item.replace('S??? l???u:', '').strip()
                item_loader.add_value('numOfFloors', numOfFloors)

            if (item.lower().find('ch??? ?????u xe h??i') >= 0):
                garage = 1
                item_loader.add_value('garage', garage)

            if (item.lower().find('s??n v?????n') >= 0):
                garden = 1
                item_loader.add_value('garden', garden)

            if (item.lower().find('h??? b??i') >= 0):
                pool = 1
                item_loader.add_value('pool', pool)

            if (item.find('S??? ph??ng ng???:') >= 0):
                numOfBedrooms = item.replace('S??? ph??ng ng???:', '').strip()
                item_loader.add_value('numOfBedrooms', numOfBedrooms)

            if (item.find('S??? ph??ng v??? sinh:') >= 0):
                numOfToilets = item.replace('S??? ph??ng v??? sinh:', '').strip()
                item_loader.add_value('numOfToilets', numOfToilets)

        email = response.css(
            'section.agent-form div.info>figure>a').xpath('@title').get()
        item_loader.add_value('email', email)

        breadcrumb = response.css('ol.breadcrumb>li>a>span::text').getall()

        city = breadcrumb[3].replace(breadcrumb[2], '').strip()
        item_loader.add_value('city', city)

        district = breadcrumb[4].strip()
        item_loader.add_value('district', district)
        description = response.css('section#description>p::text').getall()
        description = ' '.join(description)
        item_loader.add_value('description', description)

        # print(description)
        images = response.css(
            'section#property-gallery div.owl_dots>div.owl_dot').xpath('@style').getall()
        # print(images)

        if (len(images) == 0):
            images = response.css(
                'section#property-gallery img').xpath('@src').getall()
            # print(images)
            item_loader.add_value('image', [images])
        else:
            image = []
            for item in images:
                tmp = item.split(';')[0].replace(
                    'background-image: url("', '').replace('")')
                image.append(tmp)
            item_loader.add_value('image', [image])

        item_loader.add_value('url', response.request.url)

        return item_loader.load_item()
