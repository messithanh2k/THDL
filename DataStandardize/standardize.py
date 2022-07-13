import pymongo
import pandas as pd
from util import *

# read data from database
client = pymongo.MongoClient("mongodb+srv://chimeyrock999:admin123@congthongtinbatdongsan.19hdj.mongodb.net/?retryWrites=true&w=majority")
db = client["PropertiesDatabase"]
data = db["MediatedSchemaData"]
df = pd.DataFrame(list(data.find()))
df.drop(columns=["_id"], inplace=True)


def standardize(dataframe):
    dataframe['type'] = dataframe['type'].apply(typestandard)
    dataframe['square'] = dataframe['square'].apply(area_extract)
    dataframe.dropna(subset=["square"], inplace=True)
    dataframe["price"] = dataframe.apply(price_extract, axis=1)
    dataframe.dropna(subset=["price"], inplace=True)
    dataframe = dataframe[dataframe.city == 'Hà Nội']
    dataframe = dataframe[dataframe.address != '---']
    dataframe['ward'] = dataframe['location'].apply(extract_ward)
    dataframe["postedTime"] = dataframe["postedTime"].apply(compute_time)
    dataframe.dropna(subset=["postedTime"], inplace=True)
    dataframe.drop(df[df['price'] > 10e13].index, inplace = True)
    return dataframe

# write to database
df = standardize(df)
data_ = df.to_dict("records")
target_db = client["PropertiesDatabase"]
target_collection = target_db["MediatedCleanDataDuplicate"]
target_collection.insert_many(data_)
