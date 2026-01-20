from .base_scraper import BaseScraper
from playwright.sync_api import sync_playwright
import time
import random

class LinkedInScraper(BaseScraper):
    def scrape(self):
        results = []
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # LinkedIn Guest Job Search URL
            url = f"https://www.linkedin.com/jobs/search?keywords={self.keywords}&location={self.location}"
            print(f"LinkedIn URL: {url}")
            
            try:
                page.goto(url, timeout=60000)
                time.sleep(random.uniform(2, 5))
                
                # Scroll to load more
                for _ in range(3):
                    page.mouse.wheel(0, 1000)
                    time.sleep(1)

                job_cards = page.locator('ul.jobs-search__results-list li').all()
                print(f"Found {len(job_cards)} jobs on LinkedIn")

                for i, card in enumerate(job_cards[:10]):
                    try:
                        print(f"Processing LinkedIn Card {i+1}...")
                        title_el = card.locator('h3.base-search-card__title')
                        if not title_el.is_visible():
                            print(f"Card {i+1}: Title not visible, skipping.")
                            continue
                            
                        title = title_el.inner_text().strip()
                        company = card.locator('h4.base-search-card__subtitle').inner_text().strip()
                        location = card.locator('span.job-search-card__location').inner_text().strip()
                        print(f"LinkedIn Scraped: Title='{title}', Company='{company}'")
                        link = card.locator('a.base-card__full-link').get_attribute('href')
                        
                        if link:
                            results.append({
                                "title": title,
                                "company": company,
                                "location": location,
                                "url": link.split('?')[0], # Clean URL
                                "source": "LinkedIn"
                            })
                    except Exception as e:
                        print(f"Error parsing job card: {e}")
                        continue

            except Exception as e:
                print(f"LinkedIn scrape error: {e}")
            finally:
                browser.close()
        return results
