from abc import ABC, abstractmethod

class BaseScraper(ABC):
    def __init__(self, keywords, location):
        self.keywords = keywords
        self.location = location

    @abstractmethod
    def scrape(self):
        """
        Scrapes jobs and returns a list of dictionaries:
        [{
            "title": "...",
            "company": "...",
            "location": "...",
            "url": "...",
            "source": "..."
        }]
        """
        pass
