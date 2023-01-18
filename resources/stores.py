import uuid
from flask import request
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from db import stores


blp = Blueprint("stores", __name__, description= "Operation on stores")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message= "Store not found.")

    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "Store deleted"}
        except KeyError:
            abort(404, message="Store not found")
        
    def put(self, store_id):
        store_data = request.get_json()
        try:
            stores[store_id] |= store_data
            return {"message": "Store Updated"}
        except KeyError:
            abort(404, message="Store not found")


@blp.route("/store")
class StoreList(MethodView):
    def get(self):
        return {"stores": list(stores.values())}

    def post(self):
        store_data = request.get_json()
        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(400, "Store already exist ")
        store_id = uuid.uuid4().hex
        new_store = {**store_data, "store_id": store_id}
        stores[store_id] = new_store
        return new_store
