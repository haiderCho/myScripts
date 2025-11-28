#!/usr/bin/env python3
"""
BDJobs.com Job Scraper
Author: haiderCho
Description: Scrapes job postings from bdjobs.com with advanced filtering and export options
"""

import requests
from bs4 import BeautifulSoup
import csv
import json
import argparse
import time
import sys
from typing import List, Dict, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# User agent rotation to avoid blocking
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
]


class BDJobsScraper:
    """Scraper for bdjobs.com job listings"""
    
    BASE_URL = "https://jobs.bdjobs.com"
    SEARCH_URL = f"{BASE_URL}/jobsearch.asp"
    
    def __init__(self, keyword: str, location: str = "", category: str = "", 
                 limit: int = 20, max_retries: int = 3):
        self.keyword = keyword
        self.location = location
        self.category = category
        self.limit = limit
        self.max_retries = max_retries
        self.jobs = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': USER_AGENTS[0]
        })
    
    def _make_request(self, url: str, params: Optional[Dict] = None, retry_count: int = 0) -> Optional[requests.Response]:
        """Make HTTP request with retry logic"""
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            if retry_count < self.max_retries:
                logger.warning(f"Request failed, retrying... ({retry_count + 1}/{self.max_retries})")
                time.sleep(2 ** retry_count)  # Exponential backoff
                return self._make_request(url, params, retry_count + 1)
            else:
                logger.error(f"Request failed after {self.max_retries} retries: {e}")
                return None
    
    def scrape_jobs(self) -> List[Dict]:
        """Main scraping function"""
        page = 1
        jobs_scraped = 0
        
        logger.info(f"Starting scrape for keyword: '{self.keyword}'")
        
        while jobs_scraped < self.limit:
            # Construct search parameters
            params = {
                'q': self.keyword,
                'a': page
            }
            
            if self.location:
                params['l'] = self.location
            
            logger.info(f"Scraping page {page}...")
            
            response = self._make_request(self.SEARCH_URL, params)
            if not response:
                logger.error("Failed to fetch page, stopping scrape")
                break
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find job containers
            job_containers = soup.find_all('div', class_='norm-jobs-wrapper')
            
            if not job_containers:
                logger.info("No more jobs found")
                break
            
            for container in job_containers:
                if jobs_scraped >= self.limit:
                    break
                
                job_data = self._parse_job(container)
                if job_data:
                    self.jobs.append(job_data)
                    jobs_scraped += 1
                    logger.info(f"Scraped: {job_data['title']} at {job_data['company']}")
            
            # Check for next page
            pagination = soup.find('div', id='topPagging')
            if not pagination or jobs_scraped >= self.limit:
                break
            
            page += 1
            time.sleep(1)  # Rate limiting
        
        logger.info(f"Total jobs scraped: {len(self.jobs)}")
        return self.jobs
    
    def _parse_job(self, container) -> Optional[Dict]:
        """Parse individual job posting"""
        try:
            job = {}
            
            # Job title and URL
            title_elem = container.find('div', class_='job-title-text')
            if title_elem:
                title_link = title_elem.find('a')
                job['title'] = title_link.text.strip() if title_link else "N/A"
                job['url'] = self.BASE_URL + title_link['href'] if title_link and title_link.get('href') else "N/A"
            else:
                job['title'] = "N/A"
                job['url'] = "N/A"
            
            # Company name
            comp_elem = container.find('div', class_='comp-name-text')
            job['company'] = comp_elem.text.strip() if comp_elem else "N/A"
            
            # Education requirements
            edu_elem = container.find('div', class_='edu-text-d')
            job['education'] = edu_elem.text.strip() if edu_elem else "N/A"
            
            # Experience requirements
            exp_elem = container.find('div', class_='exp-text-d')
            job['experience'] = exp_elem.text.strip() if exp_elem else "N/A"
            
            # Deadline
            dead_elem = container.find('div', class_='dead-text-d')
            job['deadline'] = dead_elem.text.strip() if dead_elem else "N/A"
            
            # Location (if available)
            loc_elem = container.find('div', class_='loc-text-d')
            job['location'] = loc_elem.text.strip() if loc_elem else self.location or "N/A"
            
            return job
            
        except Exception as e:
            logger.warning(f"Error parsing job: {e}")
            return None
    
    def save_to_csv(self, filename: str):
        """Save jobs to CSV file"""
        if not self.jobs:
            logger.warning("No jobs to save")
            return
        
        headers = ['title', 'company', 'location', 'education', 'experience', 'deadline', 'url']
        
        try:
            with open(filename, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                writer.writerows(self.jobs)
            logger.info(f"Saved {len(self.jobs)} jobs to {filename}")
        except Exception as e:
            logger.error(f"Error saving to CSV: {e}")
    
    def save_to_json(self, filename: str):
        """Save jobs to JSON file"""
        if not self.jobs:
            logger.warning("No jobs to save")
            return
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.jobs, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved {len(self.jobs)} jobs to {filename}")
        except Exception as e:
            logger.error(f"Error saving to JSON: {e}")


def main():
    parser = argparse.ArgumentParser(
        description='Scrape job postings from bdjobs.com',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python JobScraper.py --keyword "software engineer" --limit 50
  python JobScraper.py --keyword "data analyst" --location "Dhaka" --output jobs.csv
  python JobScraper.py --keyword "manager" --limit 100 --format json
        """
    )
    
    parser.add_argument('--keyword', '-k', type=str, required=True,
                        help='Job title or keyword to search for')
    parser.add_argument('--location', '-l', type=str, default="",
                        help='Job location (e.g., Dhaka, Chittagong)')
    parser.add_argument('--category', '-c', type=str, default="",
                        help='Job category (optional)')
    parser.add_argument('--limit', '-n', type=int, default=20,
                        help='Number of jobs to scrape (default: 20)')
    parser.add_argument('--output', '-o', type=str, default="bdjobs_output",
                        help='Output filename without extension (default: bdjobs_output)')
    parser.add_argument('--format', '-f', type=str, choices=['csv', 'json', 'both'],
                        default='csv', help='Output format (default: csv)')
    
    args = parser.parse_args()
    
    # Create scraper
    scraper = BDJobsScraper(
        keyword=args.keyword,
        location=args.location,
        category=args.category,
        limit=args.limit
    )
    
    # Scrape jobs
    jobs = scraper.scrape_jobs()
    
    if not jobs:
        logger.warning("No jobs were scraped")
        sys.exit(1)
    
    # Save based on format
    if args.format in ['csv', 'both']:
        scraper.save_to_csv(f"{args.output}.csv")
    
    if args.format in ['json', 'both']:
        scraper.save_to_json(f"{args.output}.json")
    
    logger.info("Scraping completed successfully!")


if __name__ == '__main__':
    main()
