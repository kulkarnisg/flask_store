from db import db

class StoreModel(db.Model):
    # This is the name of table to refer
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    tags = db.relationship("TagModel", back_populates="store", lazy="dynamic")
    items = db.relationship("ItemModel", back_populates="store", lazy="dynamic")