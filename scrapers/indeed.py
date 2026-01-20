from .base_scraper import BaseScraper
from playwright.sync_api import sync_playwright
import time
import random

class IndeedScraper(BaseScraper):
    def scrape(self):
        results = []
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Construct URL
            url = f"https://www.indeed.com/jobs?q={self.keywords}&l={self.location}"
            print(f"Indeed URL: {url}")
            
            try:
                page.goto(url, timeout=60000)
                # Anti-bot simple bypass
                time.sleep(random.uniform(2, 5)) 

                job_cards = page.locator('.job_seen_beacon').all()
                print(f"Found {len(job_cards)} jobs on Indeed")

                for card in job_cards[:10]: # Limit to 10 for now
                    try:
                        title_el = card.locator('h2.jobTitle span').first
                        if not title_el.is_visible():
                            continue
                            
                        title = title_el.inner_text()
                        company = card.locator('[data-testid="company-name"]').inner_text()
                        location = card.locator('[data-testid="text-location"]').inner_text()
                        print(f"Indeed Scraped: Title='{title}', Company='{company}'")
                        link = card.locator('h2.jobTitle a').get_attribute('href')
                        
                        if link:
                            full_link = f"https://www.indeed.com{link}"
                            results.append({
                                "title": title,
                                "company": company,
                                "location": location,
                                "url": full_link,
                                "source": "Indeed"
                            })
                    except Exception as e:
                        print(f"Error parsing job card: {e}")
                        continue
                        
            except Exception as e:
                print(f"Indeed scrape error: {e}")
            finally:
                browser.close()
        return results
