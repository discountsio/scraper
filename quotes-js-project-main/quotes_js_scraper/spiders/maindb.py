import pymongo
import requests
import json
import io

class CRUD_DB:

    name = 'new-amazon-deals'
    DB_NAME = 'd1'
    COLLECTION_NAME = 'main'
    CON = pymongo.MongoClient('mongodb+srv://mtimothyrodriguez2000:timmongo2000@cluster0.znzvtiq.mongodb.net/?retryWrites=true&w=majority')

    db = CON[DB_NAME]
    collection = db[COLLECTION_NAME]

    def check_data_in_db(self, product_name, platform):
        # Check if name and platform data already in DB
        check_data = self.collection.find({ "name":product_name, "platform": platform})
        
        for val in check_data:
            #print(val)
            if(val['_id']!=None):
                print(val['_id'])
                return True
        return False

    def insert_data_in_db(self, insert_data):
        self.collection.insert_one(insert_data)

    def update_data_in_db(self, myquery, update_data):
        self.collection.update_one(myquery, update_data)

    def get_image_url_from_db(self, product_name, platform):
        check_data = self.collection.find({ "name":product_name, "platform": platform})

        for val in check_data:
            if(val['image_url']!=None):
                return val['image_url']
        return None
    
    def get_image_id_from_db(self, product_name, platform):
        check_data = self.collection.find({ "name":product_name, "platform": platform})

        for val in check_data:
            if(val['image_id']!=None):
                return val['image_id']
        return None
