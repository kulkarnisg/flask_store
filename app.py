from flask import Flask, request
from flask_smorest import abort
from db import stores, items
import uuid

app = Flask(__name__)


# Get all stores data
@app.get("/store")  # http://127.0.0.1:5000/store
def get__all_store():
    return {"stores": list(stores.values())}

# Get all items
@app.get("/item")
def get_all_items():
    return {"items": list(items.values())}

# Create a new store
@app.post("/store")
def create_store():
    store_data = request.get_json()
    for store in stores.values():
        if store_data["name"] == store["name"]:
            abort(400, "Store already exist ")
    store_id = uuid.uuid4().hex
    new_store = {**store_data, "store_id": store_id}
    stores[store_id] = new_store
    return new_store

# Add item to store
@app.post("/item")
def create_item(): 
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


# Get details for a particular store
@app.get("/store/<string:store_id>")
def get_store_data(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message= "Store not found.")

# Get item 
@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
       abort(404, message= "Item not found.")

# Update existing Store
@app.put("/store/<string:store_id>")
def update_store(store_id):
    store_data = request.get_json()
    try:
        stores[store_id] |= store_data
        return {"message": "Store Updated"}
    except KeyError:
        abort(404, message="Store not found")


# Update existing Item
@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()
    if "price" not in item_data or "name"  not in item_data:
        abort(400, message = "Bad request. Enter price and name")
    try:
        items[item_id] = item_data
        return {"message": "Items updated"}
    except KeyError:
        abort(404, message="Item not found")


# Delete a store
@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"message": "Store deleted"}
    except KeyError:
        abort(404, message="Store not found")


# Delete item
@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message": "Item deleted"}
    except KeyError: 
        abort(404, message="Item not found")
