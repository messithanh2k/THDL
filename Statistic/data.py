from pymongo import MongoClient
import pandas as pd
from bson.objectid import ObjectId

def get_post_data(ITEM_CLIENT : MongoClient):
    item_db = ITEM_CLIENT.get_database("PropertiesDatabase")
    item_collect = item_db.get_collection("MediatedCleanData")
    data = item_collect.find({}, {"_id": 1, "property_province": 1, "property_district": 1, "property_ward": 1,
                                  "property_area": 1, "property_price": 1, "property_type": 1, "property_date": 1})
    data = pd.DataFrame(list(data))
    return data

def find_item_reduce(ITEM_CLIENT : MongoClient, id):
    item_db = ITEM_CLIENT.get_database("PropertiesDatabase")
    item_collect = item_db.get_collection("MediatedCleanData")
    data = item_collect.find_one({"_id": id}, {"_id": 1, "property_province": 1, "property_district": 1, "property_ward": 1,
                                  "property_area": 1, "property_price": 1, "property_type": 1})
    return data

def get_read_data(ITEM_CLIENT : MongoClient, USER_CLIENT: MongoClient):
    def get_date_str(val):
        return val[8:10]+"/"+val[5:7]+"/"+val[0:4]

    user_db = USER_CLIENT.get_database("UserDatabase")
    log_collect = user_db.get_collection("Log")
    log_data = log_collect.find({}, {"_id": 1, "itemId": 1, "timestamp": 1})
    log_data = list(log_data)
    data = []
    for l in log_data:
        l["itemId"] = ObjectId(l["itemId"])
        l["timestamp"] = get_date_str(l["timestamp"])
        item = find_item_reduce(ITEM_CLIENT=ITEM_CLIENT, id=l["itemId"])
        item["property_date"] = l["timestamp"]
        item["_id"] = l["_id"]
        data.append(item)
    data = pd.DataFrame(data)
    return data

def write_data(STATISTICAL_CLIENT: MongoClient, data, is_post = True):
    statistic_db = STATISTICAL_CLIENT.get_database("StatisticalData")
    if is_post:
        statistic_collect = statistic_db.get_collection("PostSumup")
    else:
        statistic_collect = statistic_db.get_collection("ReadSumup")
    statistic_collect.delete_many(filter={})
    data = data.to_dict("records")
    statistic_collect.insert_many(documents=data)