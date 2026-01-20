from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from scrapers.manager import ScraperManager
from email_service import send_job_email

def init_scheduler(app):
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=run_weekly_cycle, trigger="cron", day_of_week='tue', hour=9)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())

def run_weekly_cycle():
    print("Starting weekly cycle...")
    manager = ScraperManager()
    new_jobs = manager.run_all()
    if new_jobs:
        send_job_email(new_jobs)
    else:
        print("No new jobs found.")
