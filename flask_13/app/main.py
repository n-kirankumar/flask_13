from flask import Flask, request, jsonify
from utils import get_user_info, list_all_users, update_user_info, create_user_profile
from log import log_message
from constants import  LOG_MESSAGES

app = Flask(__name__)

@app.route('/user/<username>', methods=['GET'])
def user_info(username):
    current_user = request.args.get('current_user')
    is_admin = request.args.get('is_admin', 'false').lower() == 'true'
    try:
        user_info = get_user_info(username, current_user, is_admin)
        return jsonify(user_info), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except PermissionError as e:
        return jsonify({'error': str(e)}), 403
    except Exception as e:
        log_message('error', str(e))
        return jsonify({'error': LOG_MESSAGES['internal_server_error']}), 500

@app.route('/users', methods=['GET'])
def all_users():
    current_user = request.args.get('current_user')
    is_admin = request.args.get('is_admin', 'false').lower() == 'true'
    try:
        all_users = list_all_users(current_user, is_admin)
        return jsonify(all_users), 200
    except PermissionError as e:
        return jsonify({'error': str(e)}), 403
    except Exception as e:
        log_message('error', str(e))
        return jsonify({'error': LOG_MESSAGES['internal_server_error']}), 500

@app.route('/user/<username>', methods=['PUT'])
def create_user(username):
    user_data = request.json
    try:
        new_user = create_user_profile(username, user_data)
        return jsonify(new_user), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        log_message('error', str(e))
        return jsonify({'error': LOG_MESSAGES['internal_server_error']}), 500

@app.route('/user/<username>', methods=['PATCH'])
def update_user(username):
    user_data = request.json
    current_user = request.args.get('current_user')
    is_admin = request.args.get('is_admin', 'false').lower() == 'true'
    try:
        updated_user = update_user_info(username, user_data, current_user, is_admin)
        return jsonify(updated_user), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except PermissionError as e:
        return jsonify({'error': str(e)}), 403
    except Exception as e:
        log_message('error', str(e))
        return jsonify({'error': LOG_MESSAGES['internal_server_error']}), 500

if __name__ == "__main__":
    app.run(debug=True)
