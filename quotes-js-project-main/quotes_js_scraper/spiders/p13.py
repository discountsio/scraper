# import scrapy
# from quotes_js_scraper.items import QuoteItem
# import csv

# class P13Spider(scrapy.Spider):
#     name = 'p13'
#     urls=[]
#     with open("/Users/timothy.rodriguez/Desktop/scrape/web-scrape/quotes-js-project-main/quotes_js_scraper/spiders/url.csv", 'r') as file:
#         csvreader = csv.reader(file)
#         for row in csvreader:
#             urls.append(row[0].strip())
#     start_urls=urls

#     def parse(self, response):
#         f=open("1.txt","a")
#         p13_span = response.css('span[class^="p13nListItemId"]::attr(class)').getall()

#         if(len(p13_span)>0):
#             for span in p13_span:
#                 id=span.split("_")[1]
#                 f.write(f"{id}, {response.url}\n")
#         else:
#             f.write(f" , {response.url}\n")
#         f.close()
  