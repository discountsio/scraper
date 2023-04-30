import scrapy
from quotes_js_scraper.items import QuoteItem
from quotes_js_scraper.items_amazon_products import AmazonItem
import yaml
import time
from scrapy_playwright.page import PageMethod

class AmazonSpider(scrapy.Spider):
    name = 'amazon-deals'
    page_count = 2
    search_queries = []

    # for count_for_pagination in range(0, page_count):
    #     view_index = count_for_pagination * 60
        #search_queries.append(f"https://www.amazon.in/deals?deals-widget=%257B%2522version%2522%253A1%252C%2522viewIndex%2522%253A{view_index}%252C%2522presetId%2522%253A%252210D1E5C90B957E663AF99EF905ADBFC2%2522%252C%2522sorting%2522%253A%2522BY_SCORE%2522%257D")
    search_queries.append("https://www.amazon.in/deals?ref_=nav_cs_gb")
    start_urls = search_queries

    def __init__(self):
        self.html_file = open("response.html", 'w')
        self.fromUrl=''

    def start_requests(self):
        for query in self.search_queries:
            self.list_page_url = query #fix this
            yield scrapy.Request(query, meta=dict(
                playwright = True,
                playwright_include_page = True, 
                playwright_page_methods=[
                    #PageMethod("wait_for_timeout", 3000),
                    PageMethod("wait_for_load_state", "load"),
                    PageMethod("wait_for_load_state", "domcontentloaded"),

                    # This will make the script wait till it gets all the 60 items in the deals page get loaded
                    PageMethod('wait_for_selector', '#grid-main-container > div.a-row.Grid-module__gridSection_1SEJTeTsU88s6aVeuuekAp > div > div:nth-child(60) > div > div > div > a:nth-child(2)')
                ]
                
                #playwright_include_page = True, 
                #errback=self.errback,
            ))

    def parse(self, response):
        self.html_file.write(response.text)
        deals_category_link = response.css(".a-size-mini.a-link-normal.DealLink-module__dealLink_3v4tPYOP4qJj9bdiy0xAT.a-color-base.a-text-normal::attr(href)").getall()

        open(f"link.txt","a").write(str(deals_category_link)+"\n")
        #yield {"html":str(response.body)}
        
        #for url in deals_category_link:
        self.fromUrl=response.url
        print("deals_category_link[0]"+str(deals_category_link))
        yield scrapy.Request(deals_category_link[1], callback=self.category_landing_page)
            
    def category_landing_page(self, response):
        category_product_links = response.css(".a-size-base.a-color-base.a-link-normal.a-text-normal::attr(href)").getall()

        print("category_product_links[0]"+str(category_product_links))
        #for url in category_product_links:
        yield scrapy.Request(category_product_links[0], callback=self.parse_product_details)

    def parse_product_details(self, response):
        fetchLink = response.url
        fetchName = str(response.xpath('//*[@id="productTitle"]/text()').get()).strip()
        fetchDiscountPercentage = str(response.xpath('//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[1]/text()').extract_first()).strip()
        fetchPrizeNow = str(response.xpath('//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[2]/span[2]/span[2]/text()').extract_first()).strip()
        fetchOriginalPrize = str(response.xpath('//*[@id="corePriceDisplay_desktop_feature_div"]/div[2]/span/span[1]/span/span[2]/text()').extract_first()).strip()
        #fetchEmi = str(response.xpath('//*[@id="inemi_feature_div"]/span[2]/text()').extract()[1]).strip()

        amazonItem = AmazonItem(
            list_page_link = self.fromUrl,
            product_link = fetchLink,
            name = fetchName,
            discount_percentage = fetchDiscountPercentage,
            prize_now = fetchPrizeNow,
            original_prize = fetchOriginalPrize,
            emi = None
        )

        yield amazonItem
