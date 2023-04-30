import pymongo

client = pymongo.MongoClient("127.0.0.1", 27017)

dbase = client['testdb1']

collection = dbase['testc']

post={"name":"t"}
#collection.insert_one(post)

result = collection.find()

for res in result:
    print(res)
