import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

USER_MANAGEMENT_API_URL = "http://127.0.0.1:5000"


def get_user(username):
    current_user = request.args.get('current_user')
    is_admin = request.args.get('is_admin', 'false').lower() == 'true'

    response = requests.get(f"{USER_MANAGEMENT_API_URL}/user/{username}",
                            params={'current_user': current_user, 'is_admin': is_admin})

    if response.status_code == 200:
        return jsonify(response.json())
    elif response.status_code == 404:
        return jsonify(response.json()), 404
    elif response.status_code == 403:
        return jsonify(response.json()), 403
    else:
        return jsonify(response.json()), response.status_code


def list_users():
    current_user = request.args.get('current_user')
    is_admin = request.args.get('is_admin', 'false').lower() == 'true'

    response = requests.get(f"{USER_MANAGEMENT_API_URL}/users",
                            params={'current_user': current_user, 'is_admin': is_admin})

    if response.status_code == 200:
        return jsonify(response.json())
    elif response.status_code == 403:
        return jsonify(response.json()), 403
    else:
        return jsonify(response.json()), response.status_code


def create_user(username):
    user_data = request.json
    response = requests.put(f"{USER_MANAGEMENT_API_URL}/user/{username}", json=user_data)

    if response.status_code == 201:
        return jsonify(response.json()), 201
    elif response.status_code == 400:
        return jsonify(response.json()), 400
    else:
        return jsonify(response.json()), response.status_code


def update_user(username):
    user_data = request.json
    current_user = request.args.get('current_user')
    is_admin = request.args.get('is_admin', 'false').lower() == 'true'

    response = requests.patch(f"{USER_MANAGEMENT_API_URL}/user/{username}", json=user_data,
                              params={'current_user': current_user, 'is_admin': is_admin})

    if response.status_code == 200:
        return jsonify(response.json()), 200
    elif response.status_code == 400:
        return jsonify(response.json()), 400
    elif response.status_code == 403:
        return jsonify(response.json()), 403
    else:
        return jsonify(response.json()), response.status_code


app.add_url_rule('/get_user/<username>', 'get_user', get_user, methods=['GET'])
app.add_url_rule('/list_users', 'list_users', list_users, methods=['GET'])
app.add_url_rule('/create_user/<username>', 'create_user', create_user, methods=['PUT'])
app.add_url_rule('/update_user/<username>', 'update_user', update_user, methods=['PATCH'])

if __name__ == "__main__":
    app.run(debug=True, port=5002)
