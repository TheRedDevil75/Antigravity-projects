from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float
from database import Base
import datetime

class Job(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    company = Column(String(200), nullable=False)
    location = Column(String(200))
    url = Column(String(500), unique=True, nullable=False)
    source = Column(String(50))  # indeed, linkedin
    posted_date = Column(DateTime, default=datetime.datetime.utcnow)
    scraped_date = Column(DateTime, default=datetime.datetime.utcnow)
    is_viewed = Column(Boolean, default=False)
    relevance_score = Column(Float, default=0.0)
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "url": self.url,
            "source": self.source,
            "posted_date": self.posted_date.isoformat() if self.posted_date else None,
            "is_viewed": self.is_viewed,
            "relevance_score": self.relevance_score
        }

class Criteria(Base):
    __tablename__ = 'criteria'
    id = Column(Integer, primary_key=True)
    keywords = Column(Text, default="")  # JSON string or comma-separated
    locations = Column(Text, default="")
    email_address = Column(String(200))
    email_enabled = Column(Boolean, default=True)
    smtp_server = Column(String(100), default="smtp.gmail.com")
    smtp_port = Column(Integer, default=587)
    smtp_user = Column(String(100))
    smtp_password = Column(String(100)) # Encrypt in production!
    
    def to_dict(self):
        return {
            "keywords": self.keywords,
            "locations": self.locations,
            "email_address": self.email_address,
            "email_enabled": self.email_enabled
        }
