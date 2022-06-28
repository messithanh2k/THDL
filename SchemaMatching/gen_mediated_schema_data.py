import pymongo
import pandas as pd

CONNECT_STR = "mongodb+srv://chimeyrock999:<password>@congthongtinbatdongsan.19hdj.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(CONNECT_STR)
try:
    db = client.get_database("RealEstate")
    collection = pymongo.collection.Collection(db, "RawAlomuabannhadat")
    data = collection.aggregate([{"$sample":{'size':1000}},])
    df1 = pd.DataFrame(data)
    collection = pymongo.collection.Collection(db, "RawAlonhadat.com.vn")
    data = collection.aggregate([{"$sample": {'size': 1000}}, ])
    df2 = pd.DataFrame(data)
    collection = pymongo.collection.Collection(db, "RawBatdongsan.vn")
    data = collection.aggregate([{"$sample": {'size': 1000}}, ])
    df3 = pd.DataFrame(data)
    collection = pymongo.collection.Collection(db, "RawI-batdongsan.com")
    data = collection.aggregate([{"$sample": {'size': 1000}}, ])
    df4 = pd.DataFrame(data)
finally:
    client.close()
df1.drop("_id", axis=1, inplace=True)
df1.columns = ["property_title", "property_detail", "property_price", "property_area", "property_address", "property_type", "property_date", "property_link", "property_images"]
df2.drop(["_id", "id", "direction"], axis=1, inplace=True)
df2.columns = ["property_title", "property_detail", "property_price", "property_area", "property_address", "property_type", "property_date", "property_link", "property_images"]
df3.drop("_id", axis=1, inplace=True)
df3.columns = ["property_title", "property_detail", "property_price", "property_area", "property_address", "property_type", "property_date", "property_link", "property_images"]
df4.drop(["_id"], axis=1, inplace=True)
df4.columns = ["property_title", "property_detail", "property_price", "property_area", "property_address", "property_type", "property_date", "property_link", "property_images"]
df = pd.concat([df1, df2, df3, df4], axis=0, ignore_index=True)
data = df.to_dict("records")
CONNECT_STR = "mongodb+srv://chimeyrock999:<password>@congthongtinbatdongsan.19hdj.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECT_STR)
db = client.get_database("PropertiesDatabase")
collection = pymongo.collection.Collection(db, "MediatedSchemaData")
collection.insert_many(data)
client.close()