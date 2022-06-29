import pymongo
import pandas as pd

client = pymongo.MongoClient("mongodb+srv://chimeyrock999:admin123@congthongtinbatdongsan.19hdj.mongodb.net/?retryWrites=true&w=majority")
db = client["RealEstate"]
alomuabannhadat = db["RawAlomuabannhadat.vn"]
alonhadat = db["RawAlonhadat.com.vn"]
batdongsan = db["RawBatdongsan.vn"]
ibatdongsan = db["RawI-batdongsan.com"]
alomuabannhadat = pd.DataFrame(list(alomuabannhadat.find()))
alonhadat = pd.DataFrame(list(alonhadat.find()))
batdongsan = pd.DataFrame(list(batdongsan.find()))
ibatdongsan = pd.DataFrame(list(ibatdongsan.find()))
data = pd.concat([alomuabannhadat, alonhadat, batdongsan, ibatdongsan], axis=0, ignore_index=True)
data = data.drop(columns=["_id", "id"])
data.fillna("---", inplace=True)

data = data.to_dict("records")
target_db = client["PropertiesDatabase"]
target_collection = target_db["MediatedSchemaData"]
target_collection.insert_many(data)
client.close()
