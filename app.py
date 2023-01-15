from flask import Flask, request

app = Flask(__name__)

stores = [
    {
        "name": "My Store",
        "items": [
            {
                "name": "Chair",
                "price": 12.99
            }
        ]
    }
]

# Get all stores data
@app.get("/store")  # http://127.0.0.1:5000/store
def get_store():
    return {"stores": stores}

# Create a new store
@app.post("/store")
def create_store():
    request_data = request.get_json()
    new_store = {"name": request_data["name"],
                 "items": []}
    stores.append(new_store)
    return new_store

# Add item to store
@app.post("/store/<string:name>/item")
def add_item(name):
    request_data = request.get_json()
    for store in stores:
        if store["name"] == name:
            store["items"].append(request_data)
            return request_data
    return {"message": "Store not found"}, 404

# Get details for a particular store
@app.get("/store/<string:name>")
def get_store_data(name):
    for store in stores:
        if store["name"] == name:
            return store
    return {"message": "Store not found"}, 404

# Get items in store
@app.get("/store/<string:name>/item")
def get_store_item(name):
    for store in stores:
        if store["name"] == name:
            return store["items"]
    return {"message": "Store not found"}, 404
