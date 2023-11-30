import uuid
from flask import request
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from models import ItemModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

# from db import items, stores
from schemas import ItemSchema, ItemUpdateSchema


blp = Blueprint("items", __name__, description="Operation on items")


@blp.route("/item/<string:item_id>")
class Items(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted"}

    @blp.arguments(ItemUpdateSchema)
    @blp.response(201, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        if item:
            item.name = item_data["name"]
            item.price = item_data["price"]
        else:
            item = ItemModel(id=item_id, **item_data)
        db.session.add(item)
        db.session.commit()
        return item


@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        # It will convert db object to dict (key, value pairs)
        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except IntegrityError:
            abort(500, message="Item with same name already exist")
        except SQLAlchemyError:
            abort(500, message="An Error occured.")
        return item
