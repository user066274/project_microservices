from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
#app.run(debug=True, port=5003, host=‘0.0.0.0’)

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    role = db.Column(db.String(255), nullable=False)

db.create_all()

@app.route('/users', methods=['POST'])
def register_user():
    data = request.get_json()

    username = data.get('username', None)
    email = data.get('email', None)
    role = data.get('role', None)

    if not username or not email or not role:
        return jsonify({"error": "Missing username, email, or role"}), 400

    new_user = User(username=username, email=email, role=role)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    response = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role
    }

    return jsonify(response), 200

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()

    email = data.get('email', None)
    role = data.get('role', None)

    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    if email:
        user.email = email

    if role:
        user.role = role

    db.session.commit()

    return jsonify({"message": "User updated successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5003, host='0.0.0.0')
