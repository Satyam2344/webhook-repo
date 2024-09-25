from flask import Flask, jsonify
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import sys
from app.extensions import usersCollectionName

def validate_users_data(data):
    try:
        if isinstance(data, dict) and not data:
            return jsonify({'error': 'Invalid validate_data'})
        elif isinstance(data, dict) and data:
            return validate_password(data)
        else:
            return jsonify({'error': 'Invalid validate_data'})
    except (KeyError,ValueError) as e:
        return jsonify({'error': 'Invalid validate_data'})
        
    
def check_users_existed(data):
    try:
        isExistedUser = usersCollectionName.find_one({"email": data['email']})
        return isExistedUser
    except (KeyError,ValueError) as e:
        return jsonify({'error': 'Invalid user data or key not found!!'})
    
def validate_password(data):
    try:
        if(data['password'] and len(data['password']) > 7):
            data['password'] = generate_password_hash(data['password'])
            return validate_github_url(data)
        else:
            return jsonify({"success":False, "error":"Length of password must be more than 7"})
    except (KeyError,ValueError) as e:
        return jsonify({'error': 'Invalid value of password or key is missing!!'})

def validate_github_url(data):
    try:
        if(data['github_url']):
            return set_time(data)
        else:
            return jsonify({"success":False, "error":"github url is missing or wrong url!!"})
    except (KeyError,ValueError) as e:
        return jsonify({'error': 'github url is missing or wrong url!!'})
            
def set_time(data):
    try:
        #Set UTC datetime
        utc_now = datetime.utcnow()
        data['created_at'] = utc_now
        return save_user_data(data)
    except (KeyError,ValueError) as e:
        return jsonify({'error': 'time cannot be set!!'})
    
    
def save_user_data(data):
    try:
        insert_data_into_DB = usersCollectionName.insert_one(data)
        return jsonify({"success": True, "message":"Data inserted successfully!!"})
    except (KeyError,ValueError) as e:
        return jsonify({"success":False, 'error': 'Invalid result'})

def validate_login(data):
    try:
        if isinstance(data, dict) and not data:
            return jsonify({"success": False, 'error': 'Invalid validate_data'})
        elif isinstance(data, dict) and data:
            return check_email_password(data)
        else:
            return jsonify({"success": False, 'error': 'Invalid validate_data'})
    except (KeyError,ValueError) as e:
        return jsonify({"success": False, 'error': 'Invalid validate_data'})
    
def check_email_password(data):
    try:
        # Retrieve the user document from MongoDB
        isUserExist = usersCollectionName.find_one({"email": data['email']})
        
        # Check if the password matches the hashed password
        if isUserExist and check_password_hash(isUserExist["password"], data['password']):
            # Login successful
            return jsonify({"success": True, 'message': "Login successfully!!"})
        else:
            # Login failed
            return jsonify({"success": False, 'error': 'Login Unsuccessful!! check email or password'})
    except (KeyError,ValueError) as e:
        return jsonify({"success": False, 'error': 'Invalid validate_data'})
