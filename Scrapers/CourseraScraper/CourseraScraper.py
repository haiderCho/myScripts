#!/usr/bin/env python3
"""
Coursera Course Scraper
Author: haiderCho
Description: Scrapes course information from Coursera with multiple export formats
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import argparse
import json
import csv
import logging
from typing import List, Dict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CourseraScraper:
    """Scraper for Coursera course listings"""
    
    def __init__(self, keyword: str, page_count: int = 1, headless: bool = True):
        self.keyword = keyword
        self.page_count = page_count
        self.headless = headless
        self.driver = None
        self.wait = None
        
    def _init_driver(self):
        """Initialize Chrome WebDriver with auto-detection"""
        options = Options()
        if self.headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        try:
            # Auto-detect and download ChromeDriver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            self.wait = WebDriverWait(self.driver, 100)
            logger.info("WebDriver initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            raise
    
    def scrape_all(self) -> Dict:
        """Scrape all course information"""
        self._init_driver()
        courses_data = []
        
        try:
            logger.info(f"Searching for courses: '{self.keyword}'")
            self.driver.get(f'https://www.coursera.org/search?query={self.keyword}')
            
            for page in range(self.page_count):
                logger.info(f"Scraping page {page + 1}/{self.page_count}")
                
                courses = self.wait.until(
                    EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'main ul>li'))
                )
                
                for idx, course in enumerate(courses):
                    try:
                        title = self.driver.execute_script(
                            'return arguments[0].querySelector("h3")?.innerText', course
                        )
                        description = self.driver.execute_script(
                            'return arguments[0].querySelector("p>span")?.innerText', course
                        )
                        review = self.driver.execute_script(
                            'return arguments[0].querySelector("div:has(>svg)")?.innerText.replace("\\n\\n","⭐")', course
                        )
                        url = self.driver.execute_script(
                            'return String(arguments[0].querySelector("a")?.href)', course
                        )
                        
                        data = {
                            "id": len(courses_data),
                            "title": title or "N/A",
                            "description": description or "N/A",
                            "review": review or "N/A",
                            "url": url or "N/A"
                        }
                        courses_data.append(data)
                        
                    except Exception as e:
                        logger.warning(f"Error parsing course {idx}: {e}")
                
                # Check for next page
                if page < self.page_count - 1:
                    try:
                        next_btn = self.driver.find_element(
                            By.CSS_SELECTOR, 'button[aria-label="Next Page"]'
                        )
                        if 'disabled' in next_btn.get_attribute('class'):
                            logger.info('No more pages available')
                            break
                        next_btn.click()
                    except Exception as e:
                        logger.warning(f"Pagination error: {e}")
                        break
            
            return {
                "data": courses_data,
                "message": f"Found {len(courses_data)} courses for '{self.keyword}'"
            }
            
        except Exception as e:
            logger.error(f"Scraping error: {e}")
            return {
                "data": None,
                "message": f"No courses found for '{self.keyword}'"
            }
        finally:
            if self.driver:
                self.driver.quit()
    
    def save_to_json(self, data: Dict, filename: str):
        """Save data to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving JSON: {e}")
    
    def save_to_csv(self, data: Dict, filename: str):
        """Save data to CSV file"""
        if not data.get('data'):
            logger.warning("No data to save")
            return
        
        try:
            headers = ['id', 'title', 'description', 'review', 'url']
            with open(filename, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                writer.writerows(data['data'])
            logger.info(f"Saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving CSV: {e}")


def main():
    parser = argparse.ArgumentParser(
        description='Scrape course information from Coursera',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python CourseraScraper.py --keyword "python" --pages 5 --format json
  python CourseraScraper.py -k "machine learning" -p 3 -o courses.csv
  python CourseraScraper.py -k "data science" --format both
        """
    )
    
    parser.add_argument('--keyword', '-k', type=str, required=True,
                        help='Course keyword to search for')
    parser.add_argument('--pages', '-p', type=int, default=1,
                        help='Number of pages to scrape (default: 1)')
    parser.add_argument('--output', '-o', type=str, default='coursera_output',
                        help='Output filename without extension (default: coursera_output)')
    parser.add_argument('--format', '-f', type=str, choices=['json', 'csv', 'both', 'console'],
                        default='json', help='Output format (default: json)')
    parser.add_argument('--no-headless', action='store_true',
                        help='Show browser window (default: headless mode)')
    
    args = parser.parse_args()
    
    # Create scraper
    scraper = CourseraScraper(
        keyword=args.keyword,
        page_count=args.pages,
        headless=not args.no_headless
    )
    
    # Scrape courses
    result = scraper.scrape_all()
    
    # Output based on format
    if args.format == 'console':
        print(json.dumps(result, indent=2))
    
    if args.format in ['json', 'both']:
        scraper.save_to_json(result, f"{args.output}.json")
    
    if args.format in ['csv', 'both']:
        scraper.save_to_csv(result, f"{args.output}.csv")
    
    logger.info(result['message'])


if __name__ == "__main__":
    main()
