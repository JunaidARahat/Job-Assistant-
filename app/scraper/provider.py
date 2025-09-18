from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from pathlib import Path
from typing import List, Dict

class Provider(ABC):
    @abstractmethod
    def fetch(self, source: str = None) -> List[Dict]:
        raise NotImplementedError

class LinkedInProvider(Provider):
    def __init__(self, samples_dir: str = "data/samples/linkedin"):
        self.samples_dir = Path(samples_dir)

    def fetch(self, source: str = None) -> List[Dict]:
        results = []
        if not self.samples_dir.exists():
            return results
        for p in self.samples_dir.glob("*.html"):
            html = p.read_text(encoding="utf-8")
            soup = BeautifulSoup(html, "html.parser")

            title_tag = soup.find(['h1', 'h2']) or soup.find(class_='topcard__title')
            company_tag = soup.find('a', {'data-test-company-name': True}) or soup.find(class_='topcard__org-name-link') or soup.find(class_='company')
            location_tag = soup.find(class_='topcard__flavor--bullet') or soup.find(class_='job-location')
            desc_tag = soup.find('div', {'class': 'description__text'}) or soup.find('div', {'id': 'job-details'}) or soup.find('div', class_='description')

            title = title_tag.get_text(strip=True) if title_tag else 'Unknown'
            company = company_tag.get_text(strip=True) if company_tag else 'Unknown'
            location = location_tag.get_text(strip=True) if location_tag else 'Unknown'

            requirements = []
            if desc_tag:
                text = desc_tag.get_text(separator=' ', strip=True)
                candidates = ['Python', 'Django', 'Flask', 'FastAPI', 'Docker', 'Kubernetes', 'CI/CD', 'AWS', 'GCP', 'SQL', 'Postgres', 'React']
                for c in candidates:
                    if c.lower() in text.lower():
                        requirements.append(c)

            job = {
                'title': title,
                'company': company,
                'requirements': requirements,
                'location': location
            }
            results.append(job)
        return results

def get_provider(name: str):
    name = (name or '').lower()
    if name in ('linkedin', 'li'):
        return LinkedInProvider()
    raise ValueError(f"Unknown provider: {name}")
