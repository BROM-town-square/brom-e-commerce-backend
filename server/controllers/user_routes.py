from flask import Blueprint, jsonify, request, make_response
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from server.models.user import User
from server.models import db
from werkzeug.security import generate_password_hash, check_password_hash


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
            username = username.strip().lower()
            if User.query.filter(User.username == username, User.id != identity).first():
                return make_response(jsonify({"error": "Username already taken"}), 400)
            user.username = username

        if email:
            email = email.strip().lower()
            if User.query.filter(User.email == email, User.id != identity).first():
                return make_response(jsonify({"error": "Email already taken"}), 400)
            user.email = email

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

class UserPasswordUpdate(Resource):
    @jwt_required()
    def patch(self):
        identity = get_jwt_identity()
        user = User.query.get(identity)

        if not user:
            return make_response(jsonify({"error": "User not found"}), 404)

        data = request.get_json()
        current_password = data.get('current_password')
        new_password = data.get('new_password')

        if not current_password or not new_password:
            return make_response(jsonify({"error": "Both current and new password are required"}), 400)

        if not check_password_hash(user.password, current_password):
            return make_response(jsonify({"error": "Incorrect current password"}), 400)

        if len(new_password) < 8:
            return make_response(jsonify({"error": "Password must be at least 8 characters long"}), 400)

        if check_password_hash(user.password, new_password):
            return make_response(jsonify({"error": "New password must be different from the current one"}), 400)

        user.password = generate_password_hash(new_password)
        db.session.commit()

        return make_response(jsonify({"message": "Password updated successfully"}), 200)

class AdminUserList(Resource):
    @jwt_required()
    def get(self):
        claims = get_jwt()
        if claims.get("role") != "admin":
            return make_response(jsonify({"error": "Admin access only"}), 403)

        users = User.query.all()
        user_list = [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email
            } for user in users
        ]
        return make_response(jsonify(user_list), 200)



api.add_resource(UserProfile, '/me')
api.add_resource(UserPasswordUpdate, '/me/password')
api.add_resource(AdminUserList, '/admin/users')

