from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///supervisors.db'
#app.run(debug=True, port=5002, host=‘0.0.0.0’)

db = SQLAlchemy(app)

class Supervisor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    department = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)

db.create_all()

@app.route('/supervisors', methods=['POST'])
def add_supervisor():
    data = request.get_json()

    name = data.get('name', None)
    department = data.get('department', None)
    email = data.get('email', None)

    if not name or not department or not email:
        return jsonify({"error": "Missing name, department, or email"}), 400

    new_supervisor = Supervisor(name=name, department=department, email=email)
    db.session.add(new_supervisor)
    db.session.commit()

    return jsonify({"message": "Supervisor added successfully"}), 201

@app.route('/supervisors', methods=['GET'])
def list_supervisors():
    supervisors_list = Supervisor.query.all()
    response = []

    for supervisor in supervisors_list:
        response.append({
            'id': supervisor.id,
            'name': supervisor.name,
            'department': supervisor.department,
            'email': supervisor.email
        })

    return jsonify(response), 200

@app.route('/supervisors/<int:supervisor_id>', methods=['PUT'])
def update_supervisor(supervisor_id):
    data = request.get_json()

    name = data.get('name', None)
    department = data.get('department', None)
    email = data.get('email', None)

    supervisor = Supervisor.query.get(supervisor_id)

    if not supervisor:
        return jsonify({"error": "Supervisor not found"}), 404

    if name:
        supervisor.name = name

    if department:
        supervisor.department = department

    if email:
        supervisor.email = email

    db.session.commit()

    return jsonify({"message": "Supervisor updated successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5002, host='0.0.0.0')
