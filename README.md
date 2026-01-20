# JobHunter AI - Local Job Scraper

A locally hosted web application that scarpes job sites (Indeed, LinkedIn) and notifies you of relevant opportunities.

## Features
- **Smart Scraping**: Uses Playwright to handle dynamic content.
- **Dashboard**: Track opportunities in a clean, modern UI.
- **Weekly Emails**: Automated digest sent every Tuesday at 9 AM.
- **Dockerized**: Easy to run on any platform.

## Quick Start (Docker)

1. **Prerequisites**: Install [Docker Desktop](https://www.docker.com/products/docker-desktop).
2. **Run**:
   ```bash
   docker-compose up -d
   ```
3. **Access**: Open [http://localhost:5000](http://localhost:5000).

## Manual Setup

1. Install Python 3.9+.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   playwright install
   ```
3. Run:
   ```bash
   python app.py
   ```

## Configuration

Navigate to the **Settings** page in the UI to configure:
- Search Keywords
- Target Locations
- Email Credentials (SMTP)
