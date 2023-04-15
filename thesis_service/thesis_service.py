from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///thesis.db'
#app.run(debug=True, port=5001, host='0.0.0.0')

db = SQLAlchemy(app)

class Thesis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    supervisor_id = db.Column(db.Integer, nullable=True)

db.create_all()

@app.route('/thesis', methods=['POST'])
def add_thesis():
    data = request.get_json()

    title = data.get('title', None)
    description = data.get('description', None)

    if not title or not description:
        return jsonify({"error": "Missing title or description"}), 400

    new_thesis = Thesis(title=title, description=description)
    db.session.add(new_thesis)
    db.session.commit()

    return jsonify({"message": "Thesis proposal added successfully"}), 201

@app.route('/thesis', methods=['GET'])
def list_thesis():
    thesis_list = Thesis.query.all()
    response = []

    for thesis in thesis_list:
        response.append({
            'id': thesis.id,
            'title': thesis.title,
            'description': thesis.description,
            'supervisor_id': thesis.supervisor_id
        })

    return jsonify(response), 200

@app.route('/thesis/<int:thesis_id>', methods=['PUT'])
def update_thesis(thesis_id):
    data = request.get_json()

    title = data.get('title', None)
    description = data.get('description', None)
    supervisor_id = data.get('supervisor_id', None)

    thesis = Thesis.query.get(thesis_id)

    if not thesis:
        return jsonify({"error": "Thesis proposal not found"}), 404

    if title:
        thesis.title = title

    if description:
        thesis.description = description

    if supervisor_id is not None:
        thesis.supervisor_id = supervisor_id

    db.session.commit()

    return jsonify({"message": "Thesis proposal updated successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')
