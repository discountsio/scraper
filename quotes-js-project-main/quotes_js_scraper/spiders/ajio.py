import scrapy
from scrapy.utils.response import open_in_browser
from scrapy_playwright.page import PageMethod
from scrapy.selector import Selector

import logging
import time

class QuotesScrollSpider(scrapy.Spider):

    # logger
    logger = logging.getLogger('ajio')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler('ajio.log')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    name = 'ajio'

    def start_requests(self):
        yield scrapy.Request(
            url="https://www.ajio.com/men-jeans/c/830216001?query=%3Adiscount-desc&gridColumns=5&segmentIds=",
            meta={
                "playwright": True,
                "playwright_page_methods": [
                    #PageMethod("wait_for_selector", "#contentDiv > div > div > span"),
                    PageMethod('evaluate', "console.log('ajio spider')"),#document.querySelector('#contentDiv > div > div > span').click()"),
                    #PageMethod("wait_for_selector", ".rilrtl-products-list__link")
                ],
                "playwright_include_page": True
            },
            errback=self.close_page
        )

    async def parse(self, response):

        page = response.meta['playwright_page']

        offer_percentage = 100
        product_url_list=[]
        while(len(product_url_list) < 100):  # 2 to 10
            await page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
            s  = Selector(text=await page.content())
            product_url_list = s.css('.rilrtl-products-list__link::attr(href)').getall()

            offer = s.css('.item.rilrtl-products-list__item.item:last-child .discount::text').get().strip()
            offer_percentage = ''.join(filter(self.filter_number, offer))
            try:
                offer_percentage = int(offer_percentage)
            except:
                offer_percentage = int(float(offer_percentage))
            await page.wait_for_selector('.item.rilrtl-products-list__item.item:last-child')
            
            print(f"OFFER::{len(product_url_list)} - {offer_percentage}")
        s  = Selector(text=await page.content())
        await page.close()
        self.logger.debug(product_url_list)
        for product_url in product_url_list:
            url = f"https://www.ajio.com{product_url}"
            yield scrapy.Request(
                    url=url,
                    meta={
                        "playwright": True,
                        "playwright_page_methods": [
                            PageMethod("wait_for_selector", '//*[@id="appContainer"]/div[2]/div/div/div[2]/div/div[3]/div/h2')
                        ],
                        "playwright_include_page": True
                    },
                    callback=self.parse_product_detail,
                    errback=self.close_page
                )

    async def parse_product_detail(self, response):
        page = response.meta['playwright_page']
        #await page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
        page_content = Selector(text=await page.content())
        await page.close()

        product_url = response.url
        product_brand_name = page_content.xpath('//*[@id="appContainer"]/div[2]/div/div/div[2]/div/div[3]/div/h2/text()').get().strip()
        product_name = page_content.xpath('//*[@id="appContainer"]/div[2]/div/div/div[2]/div/div[3]/div/h1/text()').get().strip()
        price_now = page_content.xpath('//*[@id="appContainer"]/div[2]/div/div/div[2]/div/div[3]/div/div[1]/div[1]/text()').get().strip()
        old_price = page_content.xpath('//*[@id="appContainer"]/div[2]/div/div/div[2]/div/div[3]/div/div[1]/div[2]/span[2]/text()').get().strip()
        offer_percentage = page_content.xpath('//*[@id="appContainer"]/div[2]/div/div/div[2]/div/div[3]/div/div[1]/div[2]/span[3]/text()').get().strip()

        description = page_content.xpath('//*[@id="appContainer"]/div[2]/div/div/div[2]/div/div[3]/div/section/h2/ul/li/text()').getall()
        product_description = ''

        for des in description:
            product_description += f'{des}\n'
        product_description = product_description.strip()

        data = {
            'product_url': product_url,
            'product_name': product_name,
            'product_description': product_description,
        }
        
        self.logger.debug(f"{data}")

    def filter_number(self, string_value):
        
        # if(string_value == '-' or string_value == '+' or string_value == '%'):
        #     return False
        if(string_value==r'.' or string_value.isdigit()):
            return True
        else:
            return False


    async def close_page(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()