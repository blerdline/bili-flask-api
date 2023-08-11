from flask import Flask
# from routes import users_bp, customers_bp

def create_app():
    app = Flask(__name__)

    # Add any additional app configurations or extensions
    from app import routes
    app.register_blueprint(routes.bp)
    # Register the blueprints
    app.register_blueprint(routes.users_bp)
    app.register_blueprint(routes.customers_bp)
    return app