#!venv3/bin/python3
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
#from werkzeug.security import safe_str_cmp
from settings import SETTINGS
from login_info import LOGIN

from feature_commands import *
from edit_commands import get_code, save_code, add_feature, remove_feature, add_function, remove_function, get_settings, save_settings

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'rt56weqrtyuis'
app.config['JWT_HEADER_NAME'] = 'Authorization'

jwt = JWTManager(app)

@app.route('/api/auth/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    login = request.json.get('login', None)
    password = request.json.get('password', None)

    if login != LOGIN['user'] or password != LOGIN['password']:
        return jsonify({"msg": "Bad username or password - " + login + " :: " + password}), 401

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=login)
    return jsonify(token=access_token), 200



@app.route('/api/featuredit', methods=['POST'])
@jwt_required
def featuredit():
    result = {}    
    ret = { 'error_code' : '0', 'error_msg' : 'SUCCESS', 'result' : result }
    
    command = request.json['command']
    if command == 'script_language':
        result = { 'language' : 'python' }
        ret = { 'error_code' : '0', 'error_msg' : 'SUCCESS!!!!!', 'result' : result }
    elif command == 'get':
        ret = get_code(request.json)
    elif command == 'save':
        ret = save_code(request.json)
    elif command == 'add_feature':
        ret = add_feature(request.json)
    elif command == 'remove_feature':
        ret = remove_feature(request.json)
    elif command == 'add_function':
        ret = add_function(request.json)
    elif command == 'remove_function':
        ret = remove_function(request.json)
    elif command == 'get_settings':
        ret = get_settings(request.json)
    elif command == 'save_settings':
        ret = save_settings(request.json)
    else:
        result = {}
        ret = { 'error_code' : 'XCCommandNotFound', 'error_msg' : 'Command not found.', 'result' : result }

    return jsonify(ret), 200

@app.route('/api/feature', methods=['POST'])
@jwt_required
def feature():
    if not request.json or not 'command' in request.json or not 'feature' in request.json:
        abort(400)

    module = __import__(request.json['feature'])
    funct = getattr(module, request.json['command'])
    result = funct(request.json, SETTINGS)

    ret = { 'error_code' : '0', 'error_msg' : '', 'result' : result }
    return jsonify(ret), 201

if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0')
