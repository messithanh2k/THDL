from schema_matching import SchemaMatching
from joblib import load
import pymongo
import pandas as pd

matcher : SchemaMatching = load("SchemaMatching.lib")


CONNECT_STR = "mongodb+srv://chimeyrock999:<password>@congthongtinbatdongsan.19hdj.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(CONNECT_STR)
try:
    db = client.get_database("PropertiesDatabase")
    collection = pymongo.collection.Collection(db, "RawAlomuabannhadat")
    data = collection.aggregate([{"$sample":{'size':100}},])
    df1 = pd.DataFrame(data)
    collection = pymongo.collection.Collection(db, "RawBatdongsan.vn")
    data = collection.aggregate([{"$sample":{'size':100}},])
    df2 = pd.DataFrame(data)
finally:
    client.close()

result1 = matcher.matching(df1)
print("----------------------------------")
print(result1)
print("----------------------------------")

result2 = matcher.matching(df2)
print("----------------------------------")
print(result2)
print("----------------------------------")
