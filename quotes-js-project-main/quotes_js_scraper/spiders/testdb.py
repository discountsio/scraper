import pymongo
import logging

logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

connection = pymongo.MongoClient('mongodb+srv://mtimothyrodriguez2000:timmongo2000@cluster0.znzvtiq.mongodb.net/?retryWrites=true&w=majority')

DB_NAME = 'testpy'
COLLECTION_NAME = 'testcol'

db = connection[DB_NAME]

#creating a collection in the name `flipkart`
collection = db[COLLECTION_NAME]
#print(collection)
# mydict = {"name":"l2", "platform":"flipkart", "price":"200"}
# collection.insert_one(mydict)

#data = collection.find({"name":"l1", "platform":"amazon" })
data = collection.find({},{'_id': False,"name":"abc"})
for d in data:
    print(d)
    for v in d.keys():
        print(v)


# creating a database in the name `fd`

def is_db_exists(db_name):
    all_db_names = connection.list_database_names()
    if db_name in all_db_names:
        return True
    else:
        return False

def is_collection_exists(db, collection_name):
    all_collections = db.list_collection_names()
    print(all_collections)
    if collection_name in all_collections:
        return True
    else:
        return False


# DB Fields


# if(is_db_exists(DB_NAME)):
#     logging.info('DB EXISTS')
#     db = connection[DB_NAME]
#     print(connection.list_database_names())
#     if(is_collection_exists(db, COLLECTION_NAME)):
#         logging.info('COLLECTION EXISTS')
#     else:
#         logging.info('COLLECTION NOT EXISTS')
#         logging.info('CREATED COLLECTION')
#         collection = db[COLLECTION_NAME]  
# else:
#     logging.info('DB AND COLLECTION NOT EXISTS')
#     logging.info(f'CREATING DB {DB_NAME}')
#     db = connection[DB_NAME]
#     print(db)
#     logging.info(f'CREATING COLLECTION {COLLECTION_NAME}')
#     collection = db[COLLECTION_NAME]
#     if(is_db_exists(DB_NAME) and is_collection_exists(db, COLLECTION_NAME)):
#         logging.info(f'DB AND COLLECTION CREATED')












