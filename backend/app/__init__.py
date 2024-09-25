from flask import Flask
from flask_cors import CORS

from app.webhook.routes import webhook
from app.frontend.signup_page import frontend


# Creating our flask app
def create_app():

    app = Flask(__name__)
    CORS(app) 
    
    # registering all the blueprints
    app.register_blueprint(webhook)
    app.register_blueprint(frontend)
    
    return app