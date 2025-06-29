from flask import Blueprint, request, jsonify, make_response
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required, get_jwt
from server.models.food_item import FoodItem
from server.models import db

food_bp = Blueprint("food", __name__)
api = Api(food_bp)

def admin_required():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return False
    return True

class FoodList(Resource):
    def get(self):
        foods = FoodItem.query.all()
        return make_response(jsonify([food.to_dict() for food in foods]), 200)

    @jwt_required()
    def post(self):
        if not admin_required():
            return make_response(jsonify({"error": "Admin access only"}), 403)

        data = request.get_json()
        name = data.get("name")
        description = data.get("description")
        price = data.get("price")
        image_url = data.get("image_url")
        category = data.get("category")

        if not all([name, price]):
            return make_response(jsonify({"error": "Name and price are required"}), 400)

        food = FoodItem(
            name=name,
            description=description,
            price=price,
            image_url=image_url,
            category=category,
        )

        db.session.add(food)
        db.session.commit()
        return make_response(jsonify(food.to_dict()), 201)

class FoodDetail(Resource):
    def get(self, id):
        food = FoodItem.query.get(id)
        if not food:
            return make_response(jsonify({"error": "Food item not found"}), 404)
        return make_response(jsonify(food.to_dict()), 200)

    @jwt_required()
    def patch(self, id):
        if not admin_required():
            return make_response(jsonify({"error": "Admin access only"}), 403)

        food = FoodItem.query.get(id)
        if not food:
            return make_response(jsonify({"error": "Food item not found"}), 404)

        data = request.get_json()
        for field in ["name", "description", "price", "image_url", "category"]:
            if field in data:
                setattr(food, field, data[field])

        db.session.commit()
        return make_response(jsonify(food.to_dict()), 200)

    @jwt_required()
    def delete(self, id):
        if not admin_required():
            return make_response(jsonify({"error": "Admin access only"}), 403)

        food = FoodItem.query.get(id)
        if not food:
            return make_response(jsonify({"error": "Food item not found"}), 404)

        db.session.delete(food)
        db.session.commit()
        return make_response(jsonify({"message": "Food item deleted"}), 200)

api.add_resource(FoodList, "")
api.add_resource(FoodDetail, "/<int:id>")
