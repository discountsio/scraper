import scrapy
from quotes_js_scraper.items import QuoteItem
from quotes_js_scraper.items_amazon_products import AmazonItem
import yaml

class AmazonSpider(scrapy.Spider):
    name = 'amazon-search'
    page_count = 1
    with open("/home/ghost/Desktop/scrape/web-scrape/quotes-js-project-main/quotes_js_scraper/spiders/amazon.yaml", "r") as yamlfile:
        data = yaml.load(yamlfile, Loader=yaml.FullLoader)
    search_keywords = data["AMAZON"]["laptop"].split(",")
    search_queries = []
    for keywords in search_keywords:
        for count_for_pagination in range(1, page_count+1):
            search_queries.append(f"https://www.amazon.in/s?k={keywords}&page={count_for_pagination}")
    #start_urls = search_queries

    def start_requests(self):
        for query in self.search_queries:
            self.list_page_url = query #fix this
            yield scrapy.Request(query, meta=dict(
                playwright = True,
                #playwright_include_page = True, 
                #errback=self.errback,
            ))

    def parse(self, response):
        
        link = response.css('.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal::attr(href)').getall()
        fileName=response.url.replace("/","|")
        open(f"{fileName}.html","wb").write(response.body)
        open(f"link.txt","a").write(str(link)+"\n")
        for url in link:
            #self.list_page_url = f"https://www.amazon.in{url}"
            yield scrapy.Request(f"https://www.amazon.in{url}", callback=self.parse_product_details, cb_kwargs=dict(from_url=response.url))
            
    def parse_product_details(self, response, from_url):
        fetchLink = response.url
        fetchName = str(response.xpath('//*[@id="productTitle"]/text()').get()).strip()
        fetchDiscountPercentage = str(response.css(".a-size-large.a-color-price.savingPriceOverride.aok-align-center.reinventPriceSavingsPercentageMargin.savingsPercentage::text").get()).strip()
        fetchPrizeNow = str(response.css(".a-price-whole::text").get()).strip()
        fetchOriginalPrize = str(response.css(".a-offscreen::text").get()).strip()
        #fetchEmi = str(response.xpath('//*[@id="inemi_feature_div"]/span[2]/text()').extract()[1]).strip()

        amazonItem = AmazonItem(
            list_page_link = from_url,
            product_link = fetchLink,
            name = fetchName,
            discount_percentage = fetchDiscountPercentage,
            prize_now = fetchPrizeNow,
            original_prize = fetchOriginalPrize,
            emi = 'fetchEmi'
        )
        #f.write(f"NAME: {n}\n")
        yield amazonItem


        #//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[37]/div/div/span/a[3]/@href


    # async def errback(self, failure):
    #     page = failure.request.meta["playwright_page"]
    #     await page.close()