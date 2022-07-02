from pymongo import MongoClient
import pandas as pd
from data import *
from statistic import *

USER_CLIENT = MongoClient("mongodb+srv://chimeyrock999:admin123@congthongtinbatdongsan.19hdj.mongodb.net/?retryWrites=true&w=majority")
ITEM_CLIENT = MongoClient("mongodb+srv://chimeyrock999:admin123@congthongtinbatdongsan.19hdj.mongodb.net/?retryWrites=true&w=majority")
STATISTICAL_CLIENT =  MongoClient("mongodb+srv://chimeyrock999:admin123@congthongtinbatdongsan.19hdj.mongodb.net/?retryWrites=true&w=majority")

try:
    data = get_read_data(ITEM_CLIENT=ITEM_CLIENT, USER_CLIENT=USER_CLIENT)
    sumup = sumup_data(data)
    write_data(STATISTICAL_CLIENT=STATISTICAL_CLIENT, data=sumup, is_post=False)
except Exception as ex:
    print(ex)
finally:
    USER_CLIENT.close()
    ITEM_CLIENT.close()
    STATISTICAL_CLIENT.close()