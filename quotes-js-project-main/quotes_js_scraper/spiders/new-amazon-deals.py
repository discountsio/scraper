import scrapy
from scrapy.utils.response import open_in_browser
from scrapy_playwright.page import PageMethod
from scrapy.selector import Selector

import pymongo
import requests
import json
import io
from quotes_js_scraper.spiders.maindb import CRUD_DB
import logging

class QuotesScrollSpider(scrapy.Spider):

    # logger
    logger = logging.getLogger('new-amazon-deals')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler('new-amazon-deals.log')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    DB = CRUD_DB()
    STRAPI_URL = 'http://localhost:1337'
    name = 'new-amazon-deals'
    platform = 'amazon'

    def start_requests(self):
        yield scrapy.Request(
            url="https://www.amazon.in/deals?ref_=nav_cs_gb",
            meta={
                "playwright": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", ".DealContent-module__truncate_sWbxETx42ZPStTc9jwySW")
                ],
                "playwright_include_page": True
            },
            errback=self.close_page
        )

    async def parse(self, response):
        page = response.meta['playwright_page']
        await page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
        # for i in range(2,11):  # 2 to 10
        #     await page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
        #     quotes_count = 10*i
        #     await page.wait_for_selector(f'.quote:nth-child({quotes_count})')
        page_content = Selector(text=await page.content())
        await page.close()
        for q in page_content.css('.DealGridItem-module__dealItemDisplayGrid_e7RQVFWSOrwXBX4i24Tqg.DealGridItem-module__withBorders_2jNNLI6U1oDls7Ten3Dttl.DealGridItem-module__withoutActionButton_2OI8DAanWNRCagYDL2iIqN'):
            # yield {
            #     'name': q.css('.DealContent-module__truncate_sWbxETx42ZPStTc9jwySW::text').get(),
            #     'category_link': q.css('.a-link-normal.DealCardDynamic-module__linkOutlineOffset_2XU8RDGmNg2HG1E-ESseNq::attr(href)').get()
            # }
            category_link=q.css('.a-size-mini.a-link-normal.DealLink-module__dealLink_3v4tPYOP4qJj9bdiy0xAT.a-color-base.a-text-normal::attr(href)').get()
            if('isPreview' in category_link or "/dp/" in category_link or "/deal/" in category_link):
                pass
            else:
                yield scrapy.Request(
                    url=category_link,
                    meta={
                        "playwright": True,
                        "playwright_page_methods": [
                            PageMethod("wait_for_selector", ".a-link-normal.s-no-outline")
                        ],
                        "playwright_include_page": True
                    },
                    callback=self.parse_product_list,
                    errback=self.close_page
                )
                break
    
    async def parse_product_list(self, response):
        page = response.meta['playwright_page']
        await page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
        page_content = Selector(text=await page.content())
        await page.close()

        product_list_link = page_content.css(".a-link-normal.s-no-outline::attr(href)").getall()
        #print(product_list_link)
        for link in product_list_link:
            yield scrapy.Request(
            url=f"https://www.amazon.in{link}",
            meta={
                "playwright": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", "#productTitle")
                ],
                "playwright_include_page": True
            },
            callback=self.parse_product_details,
            errback=self.close_page
            )

    async def parse_product_details(self, response):
        logging.warning("prod details")
        page = response.meta['playwright_page']
        await page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
        page_content = Selector(text=await page.content())
        await page.close()

        product_url = response.url
        product_name = page_content.css("#productTitle::text").get().strip()
        
        offer_percentage = page_content.xpath('//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[1]/text()').get().strip()
        offer_percentage = ''.join(filter(self.filter_number, offer_percentage))
        try:
            offer_percentage = int(offer_percentage)
        except:
            offer_percentage = int(float(offer_percentage))

        price_now = page_content.xpath('//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[2]/span[2]/span[2]/text()').get().strip()
        price_now = ''.join(filter(self.filter_number, price_now))
        try:
            price_now = int(price_now)
        except:
            price_now = int(float(price_now))
        
        old_price = page_content.xpath('//*[@id="corePriceDisplay_desktop_feature_div"]/div[2]/span/span[1]/span/span[2]/text()').get().strip()
        old_price = ''.join(filter(self.filter_number, old_price))
        try:
            old_price = int(old_price)
        except:
            old_price = int(float(old_price))
        
        rating = page_content.xpath('//*[@id="acrPopover"]/span[1]/a/i[1]/span/text()').get()
        if(rating == None):
            rating = '0'
        else:
            rating = rating.split(" ")[0].strip()
            
        rating = ''.join(filter(self.filter_number, rating))
        rating = float(rating)

        image_url = page_content.xpath('//*[@id="landingImage"]/@src').get().strip()
        description = page_content.xpath('//*[@id="feature-bullets"]/ul/li[*]/span/text()').getall()
        product_description = ''

        for des in description:
            product_description += f'{des}\n'
        product_description = product_description.strip()


        # Check if name and platform data already in DB
        data_in_db = self.DB.check_data_in_db(product_name, self.platform)
        # data_in_db = False
        # check_data = collection.find({ "name":product_name, "platform": self.platform})
        # for val in check_data:
        #     if(val['_id']!=None):
        #         data_in_db = True



        # Create or update data in DB
        if(data_in_db):
            
            if(image_url == self.DB.get_image_url_from_db(product_name, self.platform)):
                self.logger.debug(f"Image already exists - {product_url}")
                data = {
                    'url': product_url,
                    'description': 'test',#product_description,
                    'offer_percentage': offer_percentage,
                    'old_price': old_price,
                    'price_now': price_now,
                    'rating': rating,
                }

                myquery = { "name":product_name, "platform": self.platform}
                updated_data = { "$set": data }

                self.DB.update_data_in_db(myquery, updated_data)
            else:
                self.logger.debug(self.DB.get_image_url_from_db(product_name, self.platform))
                self.logger.debug(image_url)
                self.logger.debug(f"Delete image and update data - {product_url}")

                #delete image
                image_id = self.DB.get_image_id_from_db(product_name, self.platform)
                if(image_id != None):
                    response = requests.delete(f"{self.STRAPI_URL}/upload/files/{image_id}")
                    if(response.status_code == 200):
                        # image deleted successfully
                        # upload the image and get the _id
                        img_response = requests.get(image_url)
                        upload_url = 'http://localhost:1337/upload'
                        url_array=image_url.split("/")
                        image_name=f"amazon-{url_array[len(url_array)-1]}"
                        files = {'files': (image_name, img_response.content, 'image', {'uri': ''})}
                        res=requests.post(upload_url, files=files)#files=files)#, headers=headers)
                        v=res.content#.replace(b"'", b'"')
                        my_json = json.load(io.BytesIO(v))  
                        image_id = my_json[0]['_id']
                        backend_image_url = my_json[0]['url']

                        data = {
                            'url': product_url,
                            'name': product_name,
                            'description': product_description,
                            'image_url': image_url,
                            'image_name': image_name,
                            'image_id': image_id,
                            'offer_percentage': offer_percentage,
                            'old_price': old_price,
                            'price_now': price_now,
                            'rating': rating,
                            'platform': self.platform,
                            'backend_image_url': backend_image_url
                        }
                        self.DB.insert_data_in_db(data)
                    else:
                        # image not deleted or image not found
                                    # upload the image and get the _id
                        img_response = requests.get(image_url)
                        upload_url = 'http://localhost:1337/upload'
                        url_array=image_url.split("/")
                        image_name=f"amazon-{url_array[len(url_array)-1]}"
                        files = {'files': (image_name, img_response.content, 'image', {'uri': ''})}
                        res=requests.post(upload_url, files=files)#files=files)#, headers=headers)
                        v=res.content#.replace(b"'", b'"')
                        my_json = json.load(io.BytesIO(v))  
                        image_id = my_json[0]['_id']

                        data = {
                            'url': product_url,
                            'name': product_name,
                            'description': product_description,
                            'image_url': image_url,
                            'image_name': image_name,
                            'image_id': image_id,
                            'offer_percentage': offer_percentage,
                            'old_price': old_price,
                            'price_now': price_now,
                            'rating': rating,
                            'platform': self.platform
                        }
                        self.DB.insert_data_in_db(data)
        else:
            self.logger.debug(f"data created - {product_url}")

            # upload the image and get the _id
            img_response = requests.get(image_url)
            upload_url = 'http://localhost:1337/upload'
            url_array=image_url.split("/")
            image_name=f"amazon-{url_array[len(url_array)-1]}"
            files = {'files': (image_name, img_response.content, 'image', {'uri': ''})}
            res=requests.post(upload_url, files=files)#files=files)#, headers=headers)
            v=res.content#.replace(b"'", b'"')
            my_json = json.load(io.BytesIO(v))  
            image_id = my_json[0]['_id']
            backend_image_url = my_json[0]['url']

            data = {
                'url': product_url,
                'name': product_name,
                'description': product_description,
                'image_url': image_url,
                'image_name': image_name,
                'image_id': image_id,
                'offer_percentage': offer_percentage,
                'old_price': old_price,
                'price_now': price_now,
                'rating': rating,
                'platform': self.platform,
                'backend_image_url': backend_image_url
            }
            self.DB.insert_data_in_db(data)
            yield data
        
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
