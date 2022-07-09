import scrapy
from scrapy.loader import ItemLoader
from scrapy import Selector
from itemloaders.processors import TakeFirst
from batdongsan.items import BatdongsanVnItem
from scrapy.http import HtmlResponse


class BatdongsanVnSpider(scrapy.Spider):
    name = 'batdongsan_vn'
    allowed_domains = ['batdongsan.vn']
    start_urls = ['https://batdongsan.vn/ban-nha-dat-ha-noi']

    custom_settings = {
        'CLOSESPIDER_ITEMCOUNT': 1000,
        'DOWNLOAD_DELAY': 1
    }

    custom_settings = {
        'ITEM_PIPELINES': {
            'batdongsan.pipelines.BatdongsanVnPipeline': 300
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
        list_post = response.css("div .item .image > a")
        # print(list_post)
        for post in list_post:
            url = post.attrib['href']
            yield scrapy.Request(url=url, callback=self.parse_item)

        # For next page
        next_page = response.xpath("//a[contains(@rel,'next')]/@href").get()
        yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_item(self, response, **kwargs):

        item_loader = ItemLoader(item=BatdongsanVnItem(), response=response)
        item_loader.default_output_processor = TakeFirst()
        # Item

        title = response.css("h1>span::text").get()
        item_loader.add_value('title', title.strip())
        time = response.css('time.timeago').attrib['datetime']
        item_loader.add_value('postedTime', time)
        content = response.css('.body .content ::text').getall()
        content = ' '.join(content)
        item_loader.add_value('content', content)

        price = response.css("strong.price::text").getall()
        item_loader.add_value('price', ' '.join(price).strip())

        prarams = response.css('div.param>ul.uk-list>li').getall()
        for item in prarams:
            converted_item = HtmlResponse(
                url=item, body=item, encoding='utf-8')
            key = converted_item.css('strong::text').get()

            value = converted_item.css('li::text').get()
            if (key == 'Diện tích:'):
                square = value.strip()
                item_loader.add_value('square', square.strip())
            if (key == 'Địa chỉ:'):
                address = value.strip()
                item_loader.add_value('address', address.strip())
            if (key == 'Phòng ngủ:'):
                numOfBedrooms = value.strip()
                item_loader.add_value('numOfBedrooms', numOfBedrooms)
            if (key == 'Hướng nhà:'):
                direction = value.strip()
                item_loader.add_value('direction', direction)
            if (key == 'Hướng ban công:'):
                balconyDirection = value.strip()
                item_loader.add_value('balconyDirection', balconyDirection)
            if (key == 'Phòng WC:'):
                numOfToilets = value.strip()
                item_loader.add_value('numOfToilets', numOfToilets)

        author = response.css(
            'div.header > div.name > a::text').get()
        item_loader.add_value('seller', author)
        email = response.css('div.more.email > a::text').get()
        item_loader.add_value('email', email)
        phone = response.css('div.more.phone > a::text').get()
        item_loader.add_value('phone', phone)

        image = response.css('div.image.cover > a>img::attr(src)').getall()
        # print(image)
        item_loader.add_value('image', [image])
        breadcrumb = response.css('ul.uk-breadcrumb > li>a::text').getall()
        # print(breadcrumb)
        type = breadcrumb[1]
        item_loader.add_value('type', type)
        city = breadcrumb[2]
        item_loader.add_value('city', city)
        district = breadcrumb[3]
        item_loader.add_value('district', district)
        item_loader.add_value('url', response.request.url)

        return item_loader.load_item()
