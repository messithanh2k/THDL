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

ITEM_CLIENT = MongoClient('mongodb+srv://chimeyrock999:admin123@congthongtinbatdongsan.19hdj.mongodb.net/?retryWrites=true&w=majority')

@app.route('/', methods=["GET"])
def home():
    status, message, data = get_random_properties(client=ITEM_CLIENT)
    return render_template("index.html", random_data=data, formater=formater)

@app.route('/item_detail', methods=["GET"])
def item_detail_get():
    id = request.args.get("id")
    print(id)
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
if __name__ == '__main__':
    app.run(debug=True)

