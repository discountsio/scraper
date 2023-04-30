import scrapy
from quotes_js_scraper.items import QuoteItem
from quotes_js_scraper.items_amazon_products import AmazonItem
import yaml

class AmazonSpider(scrapy.Spider):
    name = 'amazon-search-bu'
    with open("/home/ghost/Desktop/scrape/web-scrape/quotes-js-project-main/quotes_js_scraper/spiders/amazon.yaml", "r") as yamlfile:
        data = yaml.load(yamlfile, Loader=yaml.FullLoader)
    search_keywords = data["AMAZON"]["laptop"].split(",")
    search_queries = []
    for keywords in search_keywords:
        search_queries.append(f"https://www.amazon.in/s?k={keywords}")
    #start_urls = search_queries
    list_page_url=''

    current_page = 1
    target_page = 3
    p=True
    def start_requests(self):
        for query in self.search_queries:
            self.list_page_url = query
            yield scrapy.Request(query, meta=dict(
                playwright = True,
                #playwright_include_page = True, 
                #errback=self.errback,
            ))

    def parse(self, response):
        #f=open("1.txt","a")
        
        link = response.css('.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal::attr(href)').getall()
        #     #quote_item['author'] = quote.css('small.author::text').get()
        #     #quote_item['tags'] = quote.css('div.tags a.tag::text').getall()
        
        # #f.write(f"{link}\n")
        # #f.write(str(response.body))

        for url in link:
            #self.list_page_url = f"https://www.amazon.in{url}"
            yield scrapy.Request(f"https://www.amazon.in{url}", callback=self.parse_product_details)
        
        # pagination
        # print("*" * 10)
        # print(self.current_page)
        # print(self.target_page)
        # print("*" * 10)
        if(self.p):
            self.current_page+=1
            next_url = response.css('.s-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator::attr(href)').get()
            self.list_page_url = next_url
            print("*" * 10)
            print(next_url)
            print("*" * 10)
            yield scrapy.Request(response.urljoin(next_url), callback=self.parse)
            
  
    def parse_product_details(self, response):
        fetchLink = response.url
        fetchName = str(response.xpath('//*[@id="productTitle"]/text()').get()).strip()
        fetchDiscountPercentage = str(response.css(".a-size-large.a-color-price.savingPriceOverride.aok-align-center.reinventPriceSavingsPercentageMargin.savingsPercentage::text").get()).strip()
        fetchPrizeNow = str(response.css(".a-price-whole::text").get()).strip()
        fetchOriginalPrize = str(response.css(".a-offscreen::text").get()).strip()
        fetchEmi = str(response.xpath('//*[@id="inemi_feature_div"]/span[2]/text()').extract()[1]).strip()

        amazonItem = AmazonItem(
            list_page_link = self.list_page_url,
            product_link = fetchLink,
            name = fetchName,
            discount_percentage = fetchDiscountPercentage,
            prize_now = fetchPrizeNow,
            original_prize = fetchOriginalPrize,
            emi = fetchEmi
        )
        #f.write(f"NAME: {n}\n")
        yield amazonItem


        #//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[37]/div/div/span/a[3]/@href


    # async def errback(self, failure):
    #     page = failure.request.meta["playwright_page"]
    #     await page.close()