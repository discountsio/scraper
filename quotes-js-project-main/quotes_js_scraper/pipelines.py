# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

# mongodb
import pymongo





class QuotesJsScraperPipeline:

    def __init__(self):
        self.conn = pymongo.MongoClient('mongodb+srv://mtimothyrodriguez2000:timmongo2000@cluster0.znzvtiq.mongodb.net/?retryWrites=true&w=majority')

        
        # creating a database in the name `fd`
        db = self.conn['fd']

        # creating a collection in the name `flipkart`
        self.collection = db['flipkart']


    # def process_item(self, item, spider):
    #     return item

    def process_item(self, amazonItem, spider):
        self.collection.insert_one(dict(amazonItem))
        return amazonItem