# import yaml

# with open("amazon.yaml", "r") as yamlfile:
#     data = yaml.load(yamlfile, Loader=yaml.FullLoader)
#     print("Read successful")
# a=data["AMAZON"]["laptop"].split(",")

# print(a)
# import pymongo
# conn = pymongo.MongoClient('localhost', 27017)

# # creating a database in the name `fd`
# db = conn['fd']
# print(db)

# # creating a collection in the name `flipkart`
# collection = db['flipkart']
# print(collection)
# mydict = {"name":"abc"}
# collection.insert_one(mydict)


###
#FOR IMAGE
###
# import requests

# image_url = "https://m.media-amazon.com/images/I/71AToeJUPBL._SX425_.jpg"
# response = requests.get(image_url)
# # with open("image.jpg", "wb") as f:
# #     f.write(response.content)
# # print(response.content)
# import json
# import io
# upload_url = 'http://localhost:1337/upload'

# url_array=image_url.split("/")

# image_name=f"amazon-{url_array[len(url_array)-1]}"

# files = {'files': (image_name, response.content, 'image', {'uri': ''})}
# res=requests.post(upload_url, files=files)#files=files)#, headers=headers)
# v=res.content#.replace(b"'", b'"')
# print(v)
# my_json = json.load(io.BytesIO(v))  
# print(my_json[0]['_id'])

# For deleting image
# import requests
# import json
# import io

# res=requests.delete("http://localhost:1337/upload/files/6427e1f822c89b36bcb594d1")
# v=res.content#.replace(b"'", b'"')
# print(v)
# my_json = json.load(io.BytesIO(v))  
# print(my_json)
# print(my_json[0]['_id'])

# #6427e1f822c89b36bcb594d1
