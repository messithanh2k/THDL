from remove_duplicate import remove_duplicate
from joblib import load
import pymongo
import pandas as pd

remover : remove_duplicate = load("RemoveDuplicate.lib")

CONNECT_STR = "mongodb+srv://chimeyrock999:<password>@congthongtinbatdongsan.19hdj.mongodb.net/?retryWrites=true&w=majority"
read_client = pymongo.MongoClient(CONNECT_STR)
read_db = read_client.get_database("PropertiesDatabase")
read_collection = pymongo.collection.Collection(read_db, "MediatedCleanDataDuplicate")

write_client = pymongo.MongoClient(CONNECT_STR)
write_db = write_client.get_database("PropertiesDatabase")
write_collection = pymongo.collection.Collection(write_db, "MediatedCleanData")

try:
    data = read_collection.find()
    df = pd.DataFrame(data)
    if len(df)>0:
        print("Original size", len(df))
        drop_ids = df["_id"].to_list()
        df = remover.remove_duplicate(df)
        print("After remove duplicates size", len(df))  
        df.drop("_id", inplace=True, axis=1)
        data = df.to_dict("records")
        write_collection.insert_many(data)
        read_collection.delete_many({"_id": {"$in": drop_ids}})
except Exception as ex:
    print(ex)
finally:
    read_client.close()
    write_client.close()
