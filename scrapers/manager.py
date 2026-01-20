from .indeed import IndeedScraper
from .linkedin import LinkedInScraper
from models import Job, Criteria
from database import db_session
from sqlalchemy.exc import IntegrityError
import datetime

class ScraperManager:
    def __init__(self):
        self.criteria = Criteria.query.first()
        if not self.criteria:
            # Default criteria if none exists
            self.keywords = "software engineer"
            self.location = "remote"
        else:
            self.keywords = self.criteria.keywords
            self.location = self.criteria.locations

    def run_all(self):
        scrapers = [
            IndeedScraper(self.keywords, self.location),
            LinkedInScraper(self.keywords, self.location)
        ]
        
        new_jobs = []
        for scraper in scrapers:
            try:
                print(f"Running {scraper.__class__.__name__}...")
                jobs = scraper.scrape()
                for job_data in jobs:
                    if self.save_job(job_data):
                        new_jobs.append(job_data)
            except Exception as e:
                print(f"Error running {scraper.__class__.__name__}: {e}")
        
        return new_jobs

    def save_job(self, job_data):
        existing = Job.query.filter_by(url=job_data['url']).first()
        if existing:
            return False
            
        job = Job(
            title=job_data['title'],
            company=job_data['company'],
            location=job_data['location'],
            url=job_data['url'],
            source=job_data['source'],
            relevance_score=self.calculate_relevance(job_data)
        )
        db_session.add(job)
        try:
            db_session.commit()
            return True
        except IntegrityError:
            db_session.rollback()
            return False

    def calculate_relevance(self, job_data):
        # Placeholder for relevance logic
        # Could use NLP or simple keyword matching
        score = 0
        title = job_data['title'].lower()
        if self.keywords.lower() in title:
            score += 10
        return score
