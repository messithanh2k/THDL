import pymongo
from joblib import load, dump
import pandas as pd
from schema_matching import SchemaMatching

READ_CONNECT_STR = "mongodb+srv://chimeyrock999:<password>@congthongtinbatdongsan.19hdj.mongodb.net/?retryWrites=true&w=majority"
WRITE_CONNECT_STR = "mongodb+srv://chimeyrock999:<password>@congthongtinbatdongsan.19hdj.mongodb.net/?retryWrites=true&w=majority"
schema_matcher = None

try:
    with open("sources.txt") as f:
        list_sources = f.readlines()
    list_sources = [x.strip() for x in list_sources]
except:
    list_sources = []

try:
    matching_results = load("MatchingResults.lib")
except:
    matching_results = {}


read_client = pymongo.MongoClient(READ_CONNECT_STR)
read_db = read_client.get_database("RealEstate")
write_client = pymongo.MongoClient(WRITE_CONNECT_STR)
write_db = write_client.get_database("PropertiesDatabase")
write_collection = pymongo.collection.Collection(write_db, "MediatedRawData")

for source in list_sources:
    try:
        read_collection = pymongo.collection.Collection(read_db, source)
        count = read_collection.count_documents({})
        if count == 0:
            continue
        if source not in matching_results:
            data = read_collection.aggregate([{"$sample":{'size':200}},])
            data = pd.DataFrame(data)
            if schema_matcher is None:
                schema_matcher : SchemaMatching = load("SchemaMatching.lib")
            matching_results[source] = schema_matcher.matching(data)
            dump(matching_results, "MatchingResults.lib")
        data = read_collection.find()
        data = pd.DataFrame(data)
        drop_ids = data["_id"].to_list()
        schema_map = matching_results[source]
        new_data = pd.DataFrame()
        for key in schema_map:
            if schema_map[key] in data.columns:
                new_data[key] = data[schema_map[key]]
            else:
                new_data[key] = ""
        new_data = new_data.to_dict("records")
        write_collection.insert_many(new_data)
        read_collection.delete_many({"_id": {"$in": drop_ids}})
    except Exception as ex:
        print(ex)

read_client.close()
write_client.close()
