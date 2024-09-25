from flask import Blueprint, json, request
from app.models import validate_data
import sys
# from app.logger import logger

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')
Push_action = 'PUSH'
Pull_action = 'PULL'
Merge_action = 'MERGE'
CONTENT_TYPE = 'application/json'

@webhook.route('/receiver', methods=["POST"])

def receiver():
    try:
        if request.headers['Content-Type'] == CONTENT_TYPE:  
            response = json.loads(json.dumps(request.json))
        if all([response.get('head_commit'), response.get('pusher')]):
                return push_webhook_handler(response)
        elif (response.get('pull_request')):
            return pull_merge_webhook_handler(response)
            # return pull_request_webhook_handler(response) if not response['pull_request']['merged'] else merge_webhook_handler(response)
        else:
                # logger.info(response)
            return False

        return {}, 200
    except (KeyError,ValueError) as e:
        return jsonify({'error': 'Invalid result'})
    
def push_webhook_handler(data):
    try:
        sendData = {};
        sendData['request_id'] = data['head_commit']['id']
        sendData['action'] = Push_action
        sendData['author'] = data['sender']['login']
        sendData['timestamp'] = data['head_commit']['timestamp']
        sendData['from_branch'] = data['ref'].split('/')[-1]
        sendData['to_branch'] = data['ref'].split('/')[-1]
        sendData['owner_url'] = data['repository']['owner']['html_url']
        return validate_data(sendData)
    except (KeyError,ValueError) as e:
        return jsonify({'error': 'Invalid result'})

def pull_merge_webhook_handler(data):
    try:
        sendData = {};
        if(data['pull_request']['merged'] and data['pull_request']['merge_commit_sha']):
            sendData['request_id'] = data['pull_request']['merge_commit_sha']
            sendData['action'] = Merge_action
            sendData['timestamp'] = data['pull_request']['merged_at']
        else:
            sendData['request_id'] = data['pull_request']['head']['sha']
            sendData['action'] = Pull_action
            sendData['timestamp'] = data['pull_request']['updated_at']
        sendData['author'] = data['sender']['login']
        sendData['from_branch'] = data['pull_request']['head']['ref']
        sendData['to_branch'] = data['pull_request']['base']['ref']
        sendData['owner_url'] = data['repository']['owner']['html_url']
        return validate_data(sendData)
    except (KeyError,ValueError) as e:
        return jsonify({'error': 'Invalid result'})
        
        
    
    
# def pull_request_webhook_handler(data):
#     try:
#         sendData = {};
#         sendData['request_id'] = data['pull_request']['head']['sha']
#         sendData['action'] = Pull_action
#         sendData['author'] = data['sender']['login']
#         sendData['timestamp'] = data['pull_request']['updated_at']
#         sendData['from_branch'] = data['pull_request']['head']['ref']
#         sendData['to_branch'] = data['pull_request']['base']['ref']
#         sendData['owner_url'] = data['repository']['owner']['html_url']
#         # print(sendData)
#         # exit()
#         return validate_data(sendData)
#     except (KeyError,ValueError) as e:
#         # logger.error(f"Error: {e}")
#         return jsonify({'error': 'Invalid result'})
    
# def merge_webhook_handler(data):
    try:
        sendData = {};
        sendData['request_id'] = data['pull_request']['merge_commit_sha']
        sendData['action'] = Merge_action
        sendData['author'] = data['sender']['login']
        sendData['timestamp'] = data['pull_request']['merged_at']
        sendData['from_branch'] = data['pull_request']['head']['ref']
        sendData['to_branch'] = data['pull_request']['base']['ref']
        sendData['owner_url'] = data['repository']['owner']['html_url']
        # print(sendData)
        # exit()
        return validate_data(sendData)
    except (KeyError,ValueError) as e:
        # logger.error(f"Error: {e}")
        return jsonify({'error': 'Invalid result'})