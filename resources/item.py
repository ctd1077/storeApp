import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import items

blp = Blueprint("items", __name__, description="Operations on items")

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    def get_item(self, item_id):
        try:
            return items[item_id], 200
        except KeyError:
            abort(404, message="Item not found.")

    def update_item(self, item_id):
        item_data = request.get_json()
        if ("price" not in item_data or "name" not in item_data):
            abort(400, message=f'Bad request. Ensure "Price" and "Name" are inculded in the JSON payload.')
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
    def get_all_items(self):
        return {"items": list(items.values())}, 200

    def create_item(self):
        item_data = request.get_json()
        if ("price" not in item_data or "store_id" not in item_data or "name" not in item_data):
            abort(400, message=f'Bad request. Ensure "Price", "Store_ID", and "Name" are inculded in the JSON payload.')

        for item in items.values():
            if (item_data["name"] == item['name'] and item_data["store_id"] == item["store_id"]):
                abort(400, message="Item already exists.")

        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item

        return item