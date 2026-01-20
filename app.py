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
        criteria = Criteria.query.first()
        if not criteria:
            criteria = Criteria()
            db_session.add(criteria)
        
        criteria.keywords = data.get('keywords')
        criteria.locations = data.get('locations')
        criteria.email_enabled = data.get('email_enabled', False)
        criteria.email_address = data.get('email_address')
        criteria.smtp_server = data.get('smtp_server')
        criteria.smtp_port = int(data.get('smtp_port', 587))
        criteria.smtp_user = data.get('smtp_user')
        criteria.smtp_password = data.get('smtp_password')
        
        db_session.commit()
        return jsonify({"status": "success"})
    
    criteria = Criteria.query.first()
    return jsonify(criteria.to_dict() if criteria else {})

@app.route('/api/scrape', methods=['POST'])
def run_scrape():
    """Manually trigger a scrape"""
    from scrapers.manager import ScraperManager
    try:
        manager = ScraperManager()
        new_jobs = manager.run_all()
        return jsonify({
            "status": "success",
            "new_jobs": len(new_jobs),
            "message": f"Found {len(new_jobs)} new jobs"
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    init_db()
    init_scheduler(app)
    app.run(host='0.0.0.0', debug=True, port=5000)
