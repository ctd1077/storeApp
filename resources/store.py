import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import stores

blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message="Store not found.")

    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "Store Deleted"}
        except KeyError:
            abort(404, message="Store not found.")

@blp.route("/store")
class StoreList(MethodView):
    def get_stores(self):
        return {"stores": list(stores.values())}

    def create_store(self):
        store_data = request.get_json()
        if ("name" not in store_data):
            abort(400, message=f'Bad request. Ensure "Name" is inculded in the JSON payload.')

        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(400, message="Store already exists.")

        store_id = uuid.uuid4().hex
        # ** is passing Keyword aguements to a constructor 
        store = {**store_data, "id":store_id}
        stores[store_id] = store
        return store, 201