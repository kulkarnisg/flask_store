import uuid
from flask import request
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from db import items, stores
from schemas import ItemSchema, ItemUpdateSchema


blp = Blueprint("items", __name__, description= "Operation on items")


@blp.route("/item/<string:item_id>")
class Items(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message= "Item not found.")

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item Deleted"}
        except KeyError:
            abort(404, message="Item not found")
    
    @blp.arguments(ItemUpdateSchema)
    @blp.response(201, ItemSchema)
    def put(self, item_data, item_id):
        try:
            items[item_id] |= item_data
            return {"message": "Items updated"}
        except KeyError:
            abort(401, message="Item not found")

@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return items.values()

    @blp.arguments(ItemSchema)
    def post(self, item_data):
        if item_data["store_id"] not in stores:
            abort(404, message= "Store not found.")
        for item in items.values():
            if item_data["name"] == item["name"] and item_data["price"] == item["price"]:
                abort(400, "Item already exist in same store")
        item_id = uuid.uuid4().hex
        new_item = {**item_data, "item_id": item_id}
        items[item_id] = new_item
        return new_item
