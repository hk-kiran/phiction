from flask import Flask, jsonify, request

app = Flask(__name__)

# Example GET request
@app.route('/api/users', methods=['GET'])
def get_selected_images():
    # Logic to fetch users from the database
    users = [
        {'id': 1, 'name': 'John'},
        {'id': 2, 'name': 'Jane'},
        {'id': 3, 'name': 'Bob'}
    ]
    return jsonify(users)

# Example POST request
# @app.route('/api/users', methods=['POST'])
# def create_user():
#     # Logic to create a new user
#     data = request.get_json()
#     name = data['name']
#     # Save the user to the database
#     user = {'id': 4, 'name': name}
#     return jsonify(user), 201

# # Example PUT request
# @app.route('/api/users/<int:user_id>', methods=['PUT'])
# def update_user(user_id):
#     # Logic to update an existing user
#     data = request.get_json()
#     name = data['name']
#     # Update the user in the database
#     user = {'id': user_id, 'name': name}
#     return jsonify(user)

# # Example DELETE request
# @app.route('/api/users/<int:user_id>', methods=['DELETE'])
# def delete_user(user_id):
#     # Logic to delete an existing user
#     # Delete the user from the database
#     return '', 204

if __name__ == '__main__':
    app.run()