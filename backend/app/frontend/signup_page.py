from flask import Flask, request, jsonify, abort, Blueprint, Response
from markupsafe import Markup
from flask_cors import CORS
import sys, time
from app.user_models import check_users_existed, validate_users_data, validate_login
from app.models import latest_data
from flask_socketio import SocketIO, emit

frontend = Blueprint('Frontend', __name__, url_prefix='/frontend')
CORS(frontend)

# Register new users
@frontend.route("/signup", methods=["POST"])
def signup():
    try:
        data = request.get_json()  
        username = data["username"]
        email = data["email"]
        github_url = data["github_url"]
        password = data["password"]
        
        # Remove scripts from input data
        username = Markup(username).striptags()
        email = Markup(email).striptags()
        github_url = Markup(github_url).striptags()
        password = Markup(password).striptags()
    
        # Validate input data
        if(all([username, password, email, github_url])):
            new_user = {
                "username": username, "email": email, "github_url":github_url, "password": password
            }
            isExistedUser = check_users_existed(new_user)
            if isExistedUser:
                return jsonify({"success": False, "error": "User already existed!!"})
            else:
                return validate_users_data(new_user)
        else:
            return jsonify({"success": False, "error": "Something went wrong!! Try again"})
    except (KeyError,ValueError) as e:
        return jsonify({'error': 'Invalid key or value!!'})

# check Login  
@frontend.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        email = data["email"]
        password = data["password"]
        
        # Remove scripts from input data
        email = Markup(email).striptags()
        password = Markup(password).striptags()
        
        if(all([password, email])):
            user = {
                "email": email, "password": password
            }
            return validate_login(user)
        else:
            return jsonify({"success": False, "error": "Something went wrong!! Try again"})
    except (KeyError,ValueError) as e:
        return jsonify({'error': 'Invalid key or value!!'})
    
#  dashboard data sender
@frontend.route("/dashboard", methods=['POST'])
def dashboard():
    try:
        params = request.get_json()
        data = latest_data(params)
        return (data)
    except (KeyError,ValueError) as e:
        return jsonify({'error': 'Invalid key or value!!'})