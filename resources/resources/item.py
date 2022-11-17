import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import items
from schemas import ItemsSchema, ItemUpdateSchema


blp = Blueprint("Items", "items", description="Operations on items")

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemsSchema)
    def get(self, item_id):
        try:
            return items[item_id], 200
        except KeyError:
            abort(404, message="Item not found.")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemsSchema)
    def put(self, item_data, item_id):
        item_data = request.get_json()
        try:
            item = items[item_id]
            item.update(item_data)
            return item
        except KeyError:
            abort(404, message="Item not found.")

    def delete(self, item_id):
            try:
                del items[item_id]
                return {"message": "Item Deleted"}
            except KeyError:
                abort(404, message="Item not found.")

@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemsSchema(many=True))
    def get(self):
        return items.values(), 200

    @blp.arguments(ItemsSchema)
    @blp.response(201, ItemsSchema)
    def post(self, item_data):
        for item in items.values():
            if (item_data["name"] == item['name'] and item_data["store_id"] == item["store_id"]):
                abort(400, message="Item already exists.")

        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item

        return item