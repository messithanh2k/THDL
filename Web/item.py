from pymongo import MongoClient
import re
import random
import uuid
import os
from pydrive.drive import GoogleDrive
from werkzeug.datastructures import FileStorage

def find_properties(client : MongoClient, filter = {}, sort = {"property_linux": -1}, offset = 0, limit=15):
    try:
        sort_list = []
        search = False

        if "property_search" in filter:
            query_str = filter["property_search"]
            filter["$text"] = {"$search": query_str}
            filter.pop('property_search', None)
            sort_list.append(('score', {'$meta': 'textScore'}))
            search = True

        db = client.get_database("PropertiesDatabase")
        collection = db.get_collection("MediatedCleanData")

        for key in sort:
            sort_list.append((key, sort[key]))

        if search:
            data = collection.find(filter, {'score': {'$meta': 'textScore'},}).sort(sort_list).skip(skip=offset).limit(limit=limit)
        else:
            data = collection.find(filter = filter).sort(sort_list).skip(skip=offset).limit(limit=limit)

        data = list(data)
        if len(data)>0:
            for x in data:
                x["_id"] = str(x["_id"])
            return True, "Lấy dữ liệu thành công", data
        else:
            return False, "Không có dữ liệu tin bài", []
    except Exception as ex:
        print("Exception in find items from database", ex)
        return False, "Lỗi database server. Lấy dữ liệu thất bại", None

def get_random_properties(client: MongoClient, limit=6):
    try:
        db = client.get_database("PropertiesDatabase")
        collection = db.get_collection("MediatedCleanData")
        data = collection.aggregate([{"$sample": {'size': limit}}, ])
        data = list(data)
        if len(data)>0:            
            for x in data:
                x["_id"] = str(x["_id"])
            return True, "Lấy dữ liệu thành công", data
        else:
            return False, "Không có dữ liệu tin bài", []
    except Exception as ex:
        print("Exception in get random items from database", ex)
        return False, "Lỗi database server. Lấy dữ liệu thất bại", None

def count_properties(client : MongoClient, filter = {}):
    try:
        if "property_search" in filter:
            query_str = filter["property_search"]
            filter["$text"] = {"$search": query_str}
            filter.pop('property_search', None)
        db = client.get_database("PropertiesDatabase")
        collection = db.get_collection("MediatedCleanData")
        count = collection.count_documents(filter=filter)
        return True, "Đếm thành công", count
    except:
        return False, "Lỗi database server. Đếm thất bại", 0

def get_property(client: MongoClient, id):
    try:
        db = client.get_database("PropertiesDatabase")
        collection = db.get_collection("MediatedCleanData")
        data = collection.find_one(filter={"_id": id})
        if data:
            data["_id"] = str(data["_id"])
            return True, "Tìm kiếm thành công", data
        else:
            return False, "ID bị sai", None
    except:
        return False, "Lỗi database server. Đếm thất bại", None

def get_near_by_properties(client: MongoClient, ward, district, province, type, limit=8):
    try:
        status, message, data = find_properties(client=client, filter={"property_ward": ward, "property_district": district,
                                                                       "property_province": province, "property_type": type},
                                                sort={"property_linux": -1}, limit=limit)
        size = len(data)
        if size<limit:
            status, message, data_add = find_properties(client=client,
                                                     filter={"property_district": district, "property_province": province,
                                                             "property_type": type},
                                                     sort={"property_linux": -1}, limit=limit-size)
            data = data + data_add
            size = len(data)
            if size<limit:
                status, message, data_add = find_properties(client=client,
                                                            filter={"province": province, "type": type},
                                                            sort={"property_linux": -1}, limit=limit - size)
                data = data + data_add
        size = len(data)
        if size>0:
            return True, "Truy vấn tin bài thành công", data
        else:
            return False, "Không tìm thấy bất động sản gần đó", data
    except Exception as ex:
        print("Exception in get near by items from database", ex)
        return False, "Lỗi database server. Truy vấn tin bài thất bại", None

def get_list_ids(client: MongoClient, filter = {}):
    try:
        db = client.get_database("PropertiesDatabase")
        collection = db.get_collection("MediatedCleanData")
        data = collection.find(filter, {"_id": 1}).sort([("property_linux", -1)]).limit(100)
        data = list(data)
        result = []
        for x in data:
            result.append(x["_id"])
        return result
    except Exception as ex:
        print("Exception in read list ids", ex)
        return []

def get_items_by_ids(client: MongoClient, list_ids):
    try:
        db = client.get_database("PropertiesDatabase")
        collection = db.get_collection("MediatedCleanData")
        data = collection.find(filter={"_id": {"$in": list_ids}})
        data = list(data)
        for x in data:
            x["_id"] = str(x["_id"])
        return data
    except Exception as ex:
        print("Exception in get items by ids", ex)
        return []

def save_file_to_local(file_obj : FileStorage):
    try:
        new_file_name = str(uuid.uuid4()) + file_obj.filename
        save_path = os.path.join("temporary", new_file_name)
        file_obj.save(save_path)
        return save_path
    except Exception as ex:
        print("Exception in saving local file", ex)
        return None

def save_file_to_drive(drive : GoogleDrive, targetimagesavedir, file_obj : FileStorage):
    local_save_path = save_file_to_local(file_obj)
    if local_save_path is None:
        return None
    try:
        gfile = drive.CreateFile({'parents': [{'id': targetimagesavedir}], 'title': os.path.basename(local_save_path)})
        gfile.SetContentFile(local_save_path)
        gfile.Upload()
        id = gfile.metadata.get("id")
        del gfile
        return "https://drive.google.com/uc?export=view&id="+id
    except Exception as ex:
        del gfile
        print("Exception in save file in drive", ex)
        return None
    finally:
        os.remove(local_save_path)

