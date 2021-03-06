from flask import Flask, session, url_for, render_template, request, redirect, make_response
from pymongo import MongoClient
from item import *
import json
from bson.objectid import ObjectId
from format import Format
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
gauth = GoogleAuth()
drive = GoogleDrive(gauth)
TARGETIMAGEDIRID = "1cwZ6StLXH8BTQV-gH5L2tM1REvB3ftpk"

formater = Format()

app = Flask(__name__)
app.secret_key = 'BATDONGSANHANOI'

# ITEM_CLIENT = MongoClient('mongodb+srv://chimeyrock999:admin123@congthongtinbatdongsan.19hdj.mongodb.net/?retryWrites=true&w=majority')
ITEM_CLIENT = MongoClient("mongodb+srv://messithanh2k:messithanh2k@qlht.kpuwx.mongodb.net/?retryWrites=true&w=majority")
STATISTICAL_CLIENT =  MongoClient("mongodb+srv://messithanh2k:messithanh2k@qlht.kpuwx.mongodb.net/?retryWrites=true&w=majority")

@app.route('/', methods=["GET"])
def home():
    status, message, data = get_random_properties(client=ITEM_CLIENT)
    return render_template("index.html", random_data=data, formater=formater)

@app.route('/item_detail', methods=["GET"])
def item_detail_get():
    id = request.args.get("id")
    try:
        id = ObjectId(id)
        status, message, item = get_property(client=ITEM_CLIENT, id=id)
        if status:
            return render_template("properties-detail.html", item=item, formater=formater)
        else:
            return render_template("404.html")
    except Exception as ex:
        print(ex)
        return render_template("404.html")

@app.route('/near_by', methods=["POST"])
def near_by_items_post():
    ward = request.form.get('ward', "")
    district = request.form.get("district", "")
    province = request.form.get("province", "")
    type = request.form.get("type", "")
    status, message, data = get_near_by_properties(client=ITEM_CLIENT, ward=ward, district=district, province=province, type=type)
    if data is None:
        data = []
    return {"status": status, "message": message, "data": data}
    
@app.route('/find_items', methods=["POST"])
def find_items_post():
    query = request.form.get("query", "{}")
    query = json.loads(query)
    limit = query.get('limit', 15)
    offset = query.get("offset", 0)
    filter = query.get("filter", {})
    sort = query.get("sort", {"property_linux": -1})
    status, message, data = find_properties(client=ITEM_CLIENT, filter=filter,
                                            sort=sort, offset=offset, limit=limit)
    if status == False:
        data = []
    return {"status": status, "message": message, "data": data}

@app.route('/statistic', methods=["GET"])
def statistic_post():
    is_post = request.args.get("post")
    if is_post == "true":
        is_post = True
    else:
        is_post = False
    return render_template("statistic.html", is_post=is_post)

@app.route('/get_statistic', methods=["POST"])
def get_statistic_post():
    district = request.form.get("district")
    ward = request.form.get("ward")
    pro_type = request.form.get("type")
    is_post = request.form.get("post")
    day = int(request.form.get("day"))
    area_type = request.form.get("area-type")
    price_type = request.form.get("price-type")
    if is_post == "true":
        is_post = True
    else:
        is_post = False
    status, message, data = get_statistic_data(STATISTICAL_CLIENT=STATISTICAL_CLIENT, prop_type=pro_type,
                              district=district, ward=ward, is_post=is_post, day=day,
                                               area_type=area_type, price_type=price_type)
    return {"status": status, "message": message, "data": data}

@app.route('/get_sub_type', methods=["POST"])
def get_sub_type_post():
    pro_type = request.form.get("type")
    return {"area_type": AREA_TYPE_MAPPING[pro_type], "price_type": PRICE_TYPE_MAPPING[pro_type]}

if __name__ == '__main__':
    app.run(debug=True)

