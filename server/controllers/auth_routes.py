from flask import Blueprint, request, jsonify, make_response
from flask_restful import Api, Resource
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from server.models.user import User
from server.models.admin import Admin
from server.models import db
from server.models.token_blocklist import TokenBlocklist
from sqlalchemy.exc import IntegrityError
from datetime import datetime


auth_bp = Blueprint('auth', __name__)
api = Api(auth_bp)

class UserRegister(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username', '').strip().lower()
        email = data.get('email', '').strip().lower()
        password = data.get('password')

        if User.query.filter((User.username == username) | (User.email == email)).first():
            return make_response(jsonify({"error": "User already exists"}), 400)

        user = User(username=username, email=email)
        user.password = password

        try:
            db.session.add(user)
            db.session.commit()
            return make_response(jsonify({"message": "User registered successfully"}), 201)
        except IntegrityError:
            db.session.rollback()
            return make_response(jsonify({"error": "User registration failed"}), 400)

class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username', '').strip().lower()
        password = data.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.verify_password(password):
            access = create_access_token(identity={"id": user.id, "role": "user"})
            refresh = create_refresh_token(identity={"id": user.id, "role": "user"})
            return make_response(jsonify({
                "access_token": access,
                "refresh_token": refresh
            }), 200)

        return make_response(jsonify({"error": "Invalid credentials"}), 401)


class AdminRegister(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username', '').strip().lower()
        email = data.get('email', '').strip().lower()
        password = data.get('password')

        if Admin.query.filter((Admin.username == username) | (Admin.email == email)).first():
            return make_response(jsonify({"error": "Admin already exists"}), 400)

        admin = Admin(username=username, email=email)
        admin.password = password

        try:
            db.session.add(admin)
            db.session.commit()
            return make_response(jsonify({"message": "Admin registered successfully"}), 201)
        except IntegrityError:
            db.session.rollback()
            return make_response(jsonify({"error": "Admin registration failed"}), 400)

class AdminLogin(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username', '').strip().lower()
        password = data.get('password')

        admin = Admin.query.filter_by(username=username).first()

        if admin and admin.verify_password(password):
            access = create_access_token(identity={"id": admin.id, "role": "admin"})
            refresh = create_refresh_token(identity={"id": admin.id, "role": "admin"})
            return make_response(jsonify({
                "access_token": access,
                "refresh_token": refresh
            }), 200)

        return make_response(jsonify({"error": "Invalid credentials"}), 401)

class Logout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]

        try:
            db.session.add(TokenBlocklist(jti=jti, created_at=now))
            db.session.commit()
            return jsonify({"message": "Logout successful"}), 200
        except:
            return jsonify({"error": "Logout failed"}), 500

class RefreshToken(Resource):
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()
        new_access = create_access_token(identity=identity)
        return make_response(jsonify({"access_token": new_access}), 200)

api.add_resource(UserRegister, "/user/register")
api.add_resource(UserLogin, "/user/login")
api.add_resource(AdminRegister, "/admin/register")
api.add_resource(AdminLogin, "/admin/login")
api.add_resource(Logout, "/logout")
api.add_resource(RefreshToken, "/refresh")