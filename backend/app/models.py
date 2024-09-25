from flask import Flask, jsonify
from datetime import datetime, timedelta
import sys, json
from app.extensions import collectionName, usersCollectionName
from bson import ObjectId


app = Flask(__name__)

# Check which recieved from github webhook is empty or not
def validate_data(data):
    try:
        if isinstance(data, dict) and not data:
            return jsonify({'error': 'Invalid validate_data'})
        elif isinstance(data, dict) and data:
            return validate_request_id(data)
        else:
            return jsonify({'error': 'Invalid validate_data'})
    except (KeyError,ValueError) as e:
        return jsonify({'error': 'Invalid validate_data'})
    
# Check request Id is present/not and should be in right format
def validate_request_id(data):
    try:
        if(all([data.get('request_id'), data['request_id']])):
            return validate_action(data)
        else:
            return jsonify({'error': 'Invalid validate_request_id'})
    except (KeyError,ValueError) as e:
        return jsonify({'error': 'Invalid validate_request_id'})
    
# check action should be PUSH, PULL or MERGE
def validate_action(data):
    try:
        if(all([data.get('action'),  data['action']])):
            return validate_author(data)
        else:
            return jsonify({'error': 'Invalid validate_action'})
    except (KeyError,ValueError) as e:
        return jsonify({'error': 'Invalid validate_action'})

# Check author is available or not
def validate_author(data):
    try:
        if(all([data.get('author'),  data['author']])):
            return validate_branches(data)
        else:
            return jsonify({'error': 'Invalid validate_author'})
    except (KeyError,ValueError) as e:
        return jsonify({'error': 'Invalid validate_author'})
    
# check both both branch "from_branch" and "to_branch" should be present
def validate_branches(data):
    try:
        if(all([data.get('from_branch'),  data['from_branch'], data.get('to_branch'), data['to_branch']])):
            return convert_timestamp_to_UTC(data)
        else:
            return jsonify({'error': 'Invalid validate_branches'})
    except (KeyError,ValueError) as e:
        return jsonify({'error': 'Invalid validate_branches'})
    
# convert timestamp of github webhook into desired format (UTC)
def convert_timestamp_to_UTC(data):
    try:
        if(all([data.get('timestamp'), data['timestamp']])):
            timestamp_str = data['timestamp']
            date = datetime.fromisoformat(timestamp_str)
            # Convert to seconds since the Unix epoch
            data['datetime'] = int(date.timestamp())
            timestamp = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S%z')
            # convert the datetime object to the desired format
            desired_format = '%d %B %Y - %I:%M %p UTC'
            data['timestamp'] = timestamp.strftime(desired_format)
            return validate_owner_url(data)
        else:
            return jsonify({'error': 'Invalid convert_timestamp_to_UTC'})
    except (KeyError,ValueError) as e:
        return jsonify({'error': 'Invalid convert_timestamp_to_UTC'})
    
# Check github url is represent 
def validate_owner_url(data):
    try:
        if(all([data.get('owner_url'), data['owner_url']])):
            
            return save_webhooks(data)
        else:
            return jsonify({'error': 'Invalid owner_url or owner_url not found!!'})
    except (KeyError,ValueError) as e:
        return jsonify({'error': 'Invalid owner_url or owner_url not found!!'})        
        
#  check data is already present or not
def check_data_existed(data):
    try:
        isExistedData = collectionName.find_one({"request_id":data['request_id'], "action":data['action'], "from_branch":data["from_branch"], "to_branch":data['to_branch']})
        if(isExistedData == []):
            return save_webhooks(data)
        else:
            return jsonify({'error': 'action already exist!!'})
    except (KeyError,ValueError) as e:
        return jsonify({'error': 'action already exist!!'})
        
#  save data into mongoDB
def save_webhooks(data):
    try:
        insert_data_into_DB = collectionName.insert_one(data)
        return jsonify({"success": True, "message":"Data inserted successfully!!"})
    except (KeyError,ValueError) as e:
        return jsonify({'error': 'Invalid result'})
    
# get data on basis of email
def get_data_email(data):
    try:
        isExistedWebhookData = usersCollectionName.find_one({"email": data['email']})
        if(isExistedWebhookData):
            return isExistedWebhookData
        else:
            return False
    except (KeyError,ValueError) as e:
        return jsonify({'error': 'Invalid key or value!!'})

# get latest data between 15 seconds timestamps
def latest_data(data):
    try:
        # Check data is already present or not. It is used ti avoid duplicacy
        checkDataExist = get_data_email(data)
        # Query to fetch latest data
        query = {"owner_url": checkDataExist['github_url']}
        # Execute the query
        results = collectionName.find_one(query, sort=[('datetime', -1)])
            
        if(results):
            json_data = json.dumps(results, cls=CustomJSONEncoder)
            return  json_data
        else:
            return jsonify({'error': 'No data found'})
            
        if(results):
            # data = list(results)
            json_data = json.dumps(results, cls=CustomJSONEncoder)
            return  json_data
        else:
            return jsonify({'error': 'No data found'})
    except (KeyError,ValueError) as e:
        return jsonify({'error': 'Invalid key or value!!'})

    
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)
    
