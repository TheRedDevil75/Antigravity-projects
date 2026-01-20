import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

try:
    print("Checking imports...")
    from app import app
    from database import init_db, db_session
    from models import Job, Criteria
    from scrapers.manager import ScraperManager
    from scheduler import init_scheduler
    print("Imports successful.")

    print("Initializing Database...")
    init_db()
    print("Database initialized.")

    print("Checking Scraper Manager instantiation...")
    manager = ScraperManager()
    print(f"Manager instantiated with keywords: {manager.keywords}")

    print("Verification passed!")
except Exception as e:
    print(f"Verification failed: {e}")
    sys.exit(1)
