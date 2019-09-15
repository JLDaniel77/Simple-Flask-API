import traceback
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


# Create item class to create item objects
class Item(Resource):

    # Create parser
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!")

    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store id.")

    # Use jwt_required decorator to require authentication on get request
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    # Create post request to make a new item
    def post(self, name):

        # Check to see if the item already exists
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        # Create data object
        data = Item.parser.parse_args()

        # Define new item and insert into items table
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            traceback.print_exc()
            return {"message": "An error occurred inserting the item"}, 500

        return item.json(), 201

    # Delete an item
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    # Update an item
    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()

        return item.json()


# Create items list
class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
