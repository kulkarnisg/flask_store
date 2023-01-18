import uuid
from flask import request
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from db import items, stores


blp = Blueprint("items", __name__, description= "Operation on items")


@blp.route("/item/<string:item_id>")
class Items(MethodView):
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message= "Item not found.")

    def delete(self):
        pass

    def put(self, item_id):
        item_data = request.get_json()
        if "price" not in item_data or "name"  not in item_data:
            abort(400, message = "Bad request. Enter price and name")
        try:
            items[item_id] |= item_data
            return {"message": "Items updated"}
        except KeyError:
            abort(404, message="Item not found")

@blp.route("/item")
class ItemList(MethodView):
    def get(self):
        return {"items": list(items.values())}

    def post(self):
        item_data = request.get_json()
        if ("name" not in item_data 
            or "price" not in item_data
            or "store_id" not in item_data):
                abort(400,
                    "Bad request, include all json data")
        if item_data["store_id"] not in stores:
            abort(404, message= "Store not found.")
        for item in items.values():
            if item_data["name"] == item["name"] and item_data["price"] == item["price"]:
                abort(400, "Item already exist in same store")
        item_id = uuid.uuid4().hex
        new_item = {**item_data, "item_id": item_id}
        items[item_id] = new_item
        return new_item
