# Job Scraper Project - Session Context

**Date:** 2026-01-20
**Current Status:** Application is runnable, accessible via web UI, settings are saving, and manual scraping is implemented.

## Recent Fixes
1.  **Database Persistence:** Fixed `sqlite3` error by mounting `data/` directory.
2.  **External Access:** Flask now listens on `0.0.0.0`, accessible at `http://<server-ip>:5000`.
3.  **Settings:** Fixed bug where settings weren't saving to DB.
4.  **Manual Scrape:** Added "Scrape Now" button to dashboard.

## Active Issue: Masked Data ("******")
- **Symptom:** Job titles and companies appear as asterisks in the UI.
- **Hypothesis:** Either LinkedIn is returning masked data, or the server was running an old version of the code without debug logs.
- **Action Taken:** Added verbose debug logging to scrapers and created `check_db.py` to inspect database directly.

## To-Do (Start Here Tomorrow)
Perform a clean update on your Linux server to ensure all debug code is running:

1.  **Update Code & Rebuild:**
    ```bash
    cd "Job application notifier"
    git pull origin main
    docker compose down
    docker compose build --no-cache  # Crucial to get new debug prints
    docker compose up -d
    ```

2.  **Trigger Scrape:**
    - Open `http://<server-ip>:5000`
    - Click **"Scrape Now"** button (top right).
    - Wait for it to finish (watch logs if possible).

3.  **Verify Data:**
    Run this command on the server to see what's actually in the database:
    ```bash
    docker exec $(docker ps -qf "name=job-scraper") python check_db.py
    ```

4.  **Check Logs:**
    If data is still masked, share the new logs:
    ```bash
    docker compose logs job-scraper > debug_logs.txt
    ```
