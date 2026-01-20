from app import app
from database import db_session
from models import Job

with app.app_context():
    jobs = Job.query.all()
    print(f"Total jobs: {len(jobs)}")
    for job in jobs:
        print(f"ID: {job.id} | Title: {job.title} | Company: {job.company} | Source: {job.source}")
