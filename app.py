from flask import Flask, request
from db import stores, items
import uuid

app = Flask(__name__)


# Get all stores data
@app.get("/store")  # http://127.0.0.1:5000/store
def get_store():
    return {"stores": list(stores.values())}

# Create a new store
@app.post("/store")
def create_store():
    store_data = request.get_json()
    store_id = uuid.uuid4().hex
    new_store = {**store_data, "store_id": store_id}
    stores[store_id] = new_store
    return new_store

# Add item to store
@app.post("/item")
def create_item(): 
    item_data = request.get_json()
    if item_data["store_id"] not in stores:
        return {"message": "Store not found"}, 404
    item_id = uuid.uuid4().hex
    new_item = {**item_data, "item_id": item_id}
    items[item_id] = new_item
    return new_item


# Get all items
@app.get("/item")
def get_all_items():
    return {"items": list(items.values())}

# Get details for a particular store
@app.get("/store/<string:store_id>")
def get_store_data(store_id):
    try:
        return stores[store_id]
    except KeyError:
        return {"message": "Store not found"}, 404

# Get items in store
@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        return {"message": "Item not found"}, 404
