from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reports.db'
#app.run(debug=True, port=5004, host=‘0.0.0.0’)

db = SQLAlchemy(app)

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    thesis_id = db.Column(db.Integer, nullable=False)
    supervisor_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)

db.create_all()

@app.route('/reports', methods=['POST'])
def add_report():
    data = request.get_json()

    thesis_id = data.get('thesis_id', None)
    supervisor_id = data.get('supervisor_id', None)
    content = data.get('content', None)

    if not thesis_id or not supervisor_id or not content:
        return jsonify({"error": "Missing thesis_id, supervisor_id, or content"}), 400

    new_report = Report(thesis_id=thesis_id, supervisor_id=supervisor_id, content=content)
    db.session.add(new_report)
    db.session.commit()

    return jsonify({"message": "Report added successfully"}), 201

@app.route('/reports', methods=['GET'])
def get_reports():
    reports = Report.query.all()
    response = []

    for report in reports:
        report_data = {
            'id': report.id,
            'thesis_id': report.thesis_id,
            'supervisor_id': report.supervisor_id,
            'content': report.content
        }
        response.append(report_data)

    return jsonify(response), 200

@app.route('/reports/<int:report_id>', methods=['PUT'])
def update_report(report_id):
    data = request.get_json()
    content = data.get('content', None)

    report = Report.query.get(report_id)

    if not report:
        return jsonify({"error": "Report not found"}), 404

    if content:
        report.content = content

    db.session.commit()

    return jsonify({"message": "Report updated successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5004, host='0.0.0.0')
