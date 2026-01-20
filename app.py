import os
from flask import Flask, render_template, jsonify, request
from database import init_db, db_session
from models import Job, Criteria
from scheduler import init_scheduler

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev_key')

# Teardown database session
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    jobs = Job.query.order_by(Job.posted_date.desc()).all()
    return jsonify([job.to_dict() for job in jobs])

@app.route('/api/criteria', methods=['GET', 'POST'])
def manage_criteria():
    if request.method == 'POST':
        data = request.json
        # TODO: Update criteria logic
        return jsonify({"status": "success"})
    
    criteria = Criteria.query.first()
    return jsonify(criteria.to_dict() if criteria else {})

if __name__ == '__main__':
    init_db()
    init_scheduler(app)
    app.run(host='0.0.0.0', debug=True, port=5000)
