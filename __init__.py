from flask import Flask, render_template


def create_app():
    app = Flask(__name__)

    from .routes import main
    app.register_blueprint(main)

    return app
