import uuid
from flask import request
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from models import StoreModel
from db import db
from schemas import StoreSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


blp = Blueprint("stores", __name__, description= "Operation on stores")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted"}

@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema )
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(500, message="Item with same name already exist")
        except SQLAlchemyError:
            abort(500, message="An Error occured.")
        return store
