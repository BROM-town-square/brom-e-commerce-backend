from flask import Blueprint, jsonify, request, make_response
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from server.models.user import User
from server.models import db

user_bp = Blueprint('user', __name__)
api = Api(user_bp)

class UserProfile(Resource):
    @jwt_required()
    def get(self):
        identity = get_jwt_identity()
        user = User.query.get(identity)

        if not user:
            return make_response(jsonify({"error": "User not found"}), 404)

        return make_response(jsonify({
            "id": user.id,
            "username": user.username,
            "email": user.email
        }), 200)

    @jwt_required()
    def patch(self):
        identity = get_jwt_identity()
        user = User.query.get(identity)

        if not user:
            return make_response(jsonify({"error": "User not found"}), 404)

        data = request.get_json()
        username = data.get('username')
        email = data.get('email')

        if username:
            user.username = username.strip().lower()
        if email:
            user.email = email.strip().lower()

        db.session.commit()
        return make_response(jsonify({"message": "Profile updated successfully"}), 200)

    @jwt_required()
    def delete(self):
        identity = get_jwt_identity()
        user = User.query.get(identity)

        if not user:
            return make_response(jsonify({"error": "User not found"}), 404)

        db.session.delete(user)
        db.session.commit()

        return make_response(jsonify({"message": "User account deleted"}), 200)


api.add_resource(UserProfile, '/me')