from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(SECRET_KEY='dev')

    # Import and register blueprints or routes
    from .routes import main_bp
    app.register_blueprint(main_bp)

    @app.errorhandler(404)
    def not_found(e):
        return {"error": "Page not found"}, 404

    return app
