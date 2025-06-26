from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .models import db
from .models.token_blocklist import TokenBlocklist
from .config import Config 

jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    
    db.init_app(app)
    jwt.init_app(app)
    migrate = Migrate(app, db)
    CORS(app, resources={r"/api/*": {"origins": [
        "http://localhost:5173", 
        "https://brom-e-commerce-front-end.onrender.com"
    ]}}, supports_credentials=True)

    
    from .controllers.auth_routes import auth_bp
    from .controllers.user_routes import user_bp
    from .controllers.food_routes import food_bp
    from .controllers.order_routes import order_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(user_bp, url_prefix="/api/users")
    app.register_blueprint(food_bp, url_prefix="/api/food")
    app.register_blueprint(order_bp, url_prefix="/api/orders")


    @app.route("/")
    def index():
        return jsonify({"message": "Taste Town API is running"}), 200

    
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(500)
    def internal_error(e):
        import traceback
        traceback.print_exc()
        return jsonify({
            "error": "Server error",
            "detail": str(e)  
        }), 500

    @jwt.unauthorized_loader
    def unauthorized_callback(err):
        return jsonify({"error": "Missing or invalid token"}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(err):
        return jsonify({"error": "Invalid token"}), 422

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"error": "Token has expired"}), 401

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        token = TokenBlocklist.query.filter_by(jti=jti).first()
        return token is not None

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({"error": "Token has been revoked"}), 401

    return app
