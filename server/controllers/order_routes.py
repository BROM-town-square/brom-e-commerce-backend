from flask import Blueprint, request, jsonify, make_response
from flask_restful import Api, Resource
from server.models.order import Order
from server.models.order_item import OrderItem
from server.models.food_item import FoodItem
from server.models import db
from flask_jwt_extended import jwt_required, get_jwt_identity

order_bp = Blueprint('orders', __name__)
api = Api(order_bp)

class UserOrders(Resource):
    @jwt_required()
    def get(self):
        user_id = int(get_jwt_identity())  
        orders = Order.query.filter_by(user_id=user_id).all()
        return make_response(jsonify([order.to_dict() for order in orders]), 200)

    @jwt_required()
    def post(self):
        user_id = int(get_jwt_identity())  
        new_order = Order(user_id=user_id)
        db.session.add(new_order)
        db.session.commit()
        return make_response(jsonify(new_order.to_dict()), 201)

class OrderItemResource(Resource):
    @jwt_required()
    def post(self, order_id):
        user_id = int(get_jwt_identity()) 

        
        order = Order.query.filter_by(id=order_id, user_id=user_id).first()
        if not order:
            return make_response(jsonify({'error': 'Order not found or unauthorized'}), 404)

        data = request.get_json()
        food_item_id = data.get('food_item_id')
        quantity = data.get('quantity', 1)

        if not food_item_id:
            return make_response(jsonify({'error': 'food_item_id is required'}), 400)

        food_item = FoodItem.query.get(food_item_id)
        if not food_item:
            return make_response(jsonify({'error': 'Food item not found'}), 404)

        order_item = OrderItem(
            order_id=order.id,
            food_item_id=food_item.id,
            quantity=quantity
        )
        db.session.add(order_item)
        db.session.commit()

        return make_response(jsonify(order_item.to_dict()), 201)


api.add_resource(UserOrders, '')
api.add_resource(OrderItemResource, '/<int:order_id>/items')
