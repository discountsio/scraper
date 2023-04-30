import scrapy
#from quotes_js_scraper.items import QuoteItem
from quotes_js_scraper.items_amazon_products import AmazonItem
import yaml
import time
from scrapy_playwright.page import PageMethod

class FlipkartSpider(scrapy.Spider):
    name = 'flipkart-deals'
    page_count = 2
    search_queries = ['https://www.flipkart.com/offers-list/content?screen=dynamic&pk=themeViews%3DDT-OMU-1%3ADealcard~widgetType%3DdealCard~contentType%3Dneo&wid=2.dealCard.OMU&wid=3.dealCard.OMU_3&otracker=hp_omu_Best%2Bof%2BElectronics_3&otracker1=hp_omu_PINNED_neo%2Fmerchandising_Best%2Bof%2BElectronics_NA_wc_view-all_3']

    # for count_for_pagination in range(0, page_count):
    #     view_index = count_for_pagination * 60
        #search_queries.append(f"https://www.amazon.in/deals?deals-widget=%257B%2522version%2522%253A1%252C%2522viewIndex%2522%253A{view_index}%252C%2522presetId%2522%253A%252210D1E5C90B957E663AF99EF905ADBFC2%2522%252C%2522sorting%2522%253A%2522BY_SCORE%2522%257D")
    start_urls = search_queries

    def start_requests(self):
        for query in self.search_queries:
            self.list_page_url = query #fix this
            yield scrapy.Request(query, meta=dict(
                playwright = True,
                playwright_include_page = True, 
                playwright_page_methods=[
                    #PageMethod("wait_for_timeout", 3000),
                    # PageMethod("wait_for_load_state", "load"),
                    # PageMethod("wait_for_load_state", "domcontentloaded"),

                    # This will make the script wait till it gets all the 60 items in the deals page get loaded
                    PageMethod('wait_for_selector', '._6WQwDJ')
                ]
                
                #playwright_include_page = True, 
                #errback=self.errback,
            ))

    def parse(self, response):
        deals_category_link = response.css("._6WQwDJ::attr(href)").getall()

        #open(f"link.txt","a").write(str(deals_category_link)+"\n")
        #yield {"html":str(response.body)}
        for link in deals_category_link:
            yield scrapy.Request(f"https://www.flipkart.com{link}", callback=self.check_category_or_product, meta=dict(sourceUrl=link))

    def check_category_or_product(self, response):
        product_link_from_card = response.css('.s1Q9rs::attr(href)').getall()
        product_link_from_list = response.css('._1fQZEK::attr(href)').getall()
        
        if(len(product_link_from_card)>0):
            open(f"1.txt","a").write(str(product_link_from_card)+"\n")
            for link in product_link_from_card:
                yield scrapy.Request(f"https://www.flipkart.com{link}", callback=self.product_details_from_page, meta=dict(sourceUrl=response.url))
        else:
            open("2.txt","a").write(str(product_link_from_list)+"\n")
            for link in product_link_from_list:
                yield scrapy.Request(f"https://www.flipkart.com{link}", callback=self.product_details_from_page, meta=dict(sourceUrl=response.url))

    def product_details_from_list(self, response):

        fetchLink = response.url
        product_link = response.css('.s1Q9rs::attr(href)').getall()
        if(len(product_link)>0):
            for link in product_link:
                yield scrapy.Request(f"https://www.flipkart.com{link}", callback=self.product_details_from_page)
        else:
            for product_div in response.css('._13oc-S'):
                fetchName = str(product_div.css('._4rR01T::text').get()).strip()
                fetchDiscountPercentage = str(response.css('._3Ay6Sb > span::text').get()).strip()
                fetchPrizeNow = str(response.css('._30jeq3._1_WHN1::text').get()).strip()
                fetchOriginalPrize = str(response.css('._3I9_wc._27UcVY::text').get()).strip()
                #fetchEmi = str(response.xpath('//*[@id="inemi_feature_div"]/span[2]/text()').extract()[1]).strip()

                amazonItem = AmazonItem(
                    list_page_link = "self.meta['sourceUrl']",
                    product_link = fetchLink,
                    name = fetchName,
                    discount_percentage = fetchDiscountPercentage,
                    prize_now = fetchPrizeNow,
                    original_prize = fetchOriginalPrize,
                    emi = None
                )

                yield amazonItem

    def product_details_from_page(self, response):
        fetchLink = response.url

        fetchName = str(response.css('.B_NuCI::text').get()).strip()
        fetchDiscountPercentage = str(response.css('._3Ay6Sb > span::text').get()).strip()
        fetchPrizeNow = str(response.css('._30jeq3._16Jk6d::text').get()).strip()
        fetchOriginalPrize = str(response.css('._3I9_wc._2p6lqe::text').getall()[1]).strip()
        fetchEmi = str(response.css('._1Ma4bX::text').get()).strip()

        amazonItem = AmazonItem(
            source_url = response.meta['sourceUrl'],
            product_link = fetchLink,
            name = fetchName,
            discount_percentage = fetchDiscountPercentage,
            prize_now = fetchPrizeNow,
            original_prize = fetchOriginalPrize,
            emi = fetchEmi
        )
        yield amazonItem
