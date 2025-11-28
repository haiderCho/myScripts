#!/usr/bin/env python3
"""
LeetCode Problem Scraper
Author: haiderCho
Description: Scrapes LeetCode problems and exports to PDF and/or Markdown
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from fpdf import FPDF
import argparse
import os
import logging
from typing import Optional, Dict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Difficulty levels
DIFFICULTY_LEVELS = {
    "Easy": "?difficulty=Easy",
    "Medium": "?difficulty=Medium",
    "Hard": "?difficulty=Hard"
}


class LeetCodeScraper:
    """Scraper for LeetCode problems"""
    
    BASE_URL = "https://leetcode.com/problemset/all"
    
    def __init__(self, category: str = "Easy", headless: bool = True, output_dir: str = "./LeetCode"):
        self.category = category
        self.headless = headless
        self.output_dir = output_dir
        self.driver = None
        self.wait = None
        
        # Create output directory
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            logger.info(f"Created output directory: {output_dir}")
    
    def _init_driver(self):
        """Initialize Chrome WebDriver"""
        options = Options()
        if self.headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.page_load_strategy = 'none'
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            self.wait = WebDriverWait(self.driver, 15)
            logger.info("WebDriver initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            raise
    
    def get_problems(self, no_of_problems: int) -> list:
        """Get problem list from LeetCode"""
        self._init_driver()
        problem_info = {}
        
        try:
            url = f"{self.BASE_URL}/{DIFFICULTY_LEVELS[self.category]}"
            logger.info(f"Fetching {self.category} problems from LeetCode...")
            self.driver.get(url)
            
            # Wait for problem table
            self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//*[@id='question-app']/div/div[2]/div[2]/div[2]/table/tbody[1]/tr[1]")
                )
            )
            
            for problem_index in range(1, no_of_problems + 1):
                try:
                    # Get problem name
                    problem_name = self.driver.find_element(
                        By.XPATH,
                        f"//*[@id='question-app']/div/div[2]/div[2]/div[2]/table/tbody[1]/tr[{problem_index}]/td[3]"
                    ).text
                    
                    # Get problem URL
                    problem_url = self.driver.find_element(
                        By.XPATH,
                        f"//*[@id='question-app']/div/div[2]/div[2]/div[2]/table/tbody[1]/tr[{problem_index}]/td[3]/div/a"
                    ).get_attribute('href')
                    
                    logger.info(f"Found: {problem_name}")
                    problem_info[problem_name] = problem_url
                    
                except Exception as e:
                    logger.warning(f"Error getting problem {problem_index}: {e}")
            
            return problem_info
            
        except TimeoutException:
            logger.error("Timeout: Page took too long to load")
            return {}
        finally:
            # Don't close driver yet, we'll use it for getting descriptions
            pass
    
    def get_description(self, problem_url: str, problem_name: str) -> Optional[Dict]:
        """Get problem description"""
        try:
            logger.info(f"Fetching description for: {problem_name}")
            self.driver.get(problem_url)
            
            self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//*[@id='app']/div/div[2]/div/div/div[1]/div/div[1]/div[1]/div/div[2]/div/div[2]/div/p[1]")
                )
            )
            
            # Get problem statement
            problem_statement = self.driver.find_element(
                By.XPATH,
                "//*[@id='app']/div/div[2]/div/div/div[1]/div/div[1]/div[1]/div/div[2]/div/div[2]/div/p[1]"
            ).text
            
            # Get test cases
            problem_test_cases = self.driver.find_element(
                By.XPATH,
                "//*[@id='app']/div/div[2]/div/div/div[1]/div/div[1]/div[1]/div/div[2]/div/div[2]/div/pre[1]"
            ).text
            
            if "Output" not in problem_test_cases:
                problem_test_cases = "Input\n" + problem_test_cases
                try:
                    output = self.driver.find_element(
                        By.XPATH,
                        "//*[@id='problem-statement']/pre[2]"
                    ).text
                    problem_test_cases += "\nOutput\n" + output
                except:
                    pass
            
            return {
                'title': problem_name,
                'statement': problem_statement,
                'test_case': problem_test_cases,
                'url': problem_url
            }
            
        except (NoSuchElementException, TimeoutException) as e:
            logger.warning(f"Could not scrape description for {problem_name}: {e}")
            return None
    
    def to_pdf(self, problem: Dict):
        """Export problem to PDF"""
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=15)
            
            # Encode to latin-1
            title = problem["title"].encode('latin-1', 'replace').decode('latin-1')
            statement = problem["statement"].encode('latin-1', 'replace').decode('latin-1')
            test_case = problem["test_case"].encode('latin-1', 'replace').decode('latin-1')
            url = problem["url"]
            
            pdf.cell(200, 10, txt=title, ln=1, align='C')
            pdf.multi_cell(200, 10, txt=statement, align='L')
            pdf.multi_cell(200, 10, txt=test_case, align='L')
            pdf.write(5, 'Problem Link: ')
            pdf.write(5, url, url)
            
            filename = os.path.join(self.output_dir, f"{title.strip()}.pdf")
            pdf.output(filename)
            logger.info(f"Saved PDF: {filename}")
            
        except Exception as e:
            logger.error(f"Error creating PDF: {e}")
    
    def to_markdown(self, problem: Dict):
        """Export problem to Markdown"""
        try:
            title = problem["title"]
            statement = problem["statement"]
            test_case = problem["test_case"]
            url = problem["url"]
            
            md_content = f"""# {title}

## Problem Statement
{statement}

## Test Cases
```
{test_case}
```

## Link
[View on LeetCode]({url})
"""
            
            filename = os.path.join(self.output_dir, f"{title.strip()}.md")
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(md_content)
            logger.info(f"Saved Markdown: {filename}")
            
        except Exception as e:
            logger.error(f"Error creating Markdown: {e}")
    
    def close(self):
        """Close WebDriver"""
        if self.driver:
            self.driver.quit()


def main():
    parser = argparse.ArgumentParser(
        description='Scrape LeetCode problems',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python LeetCodeScraper.py --difficulty Easy --count 10
  python LeetCodeScraper.py -d Medium -n 5 --format md
  python LeetCodeScraper.py -d Hard -n 3 --format both
        """
    )
    
    parser.add_argument('--difficulty', '-d', type=str, 
                        choices=['Easy', 'Medium', 'Hard'], default='Easy',
                        help='Difficulty level (default: Easy)')
    parser.add_argument('--count', '-n', type=int, default=5,
                        help='Number of problems to scrape (default: 5)')
    parser.add_argument('--format', '-f', type=str,
                        choices=['pdf', 'md', 'both'], default='pdf',
                        help='Output format (default: pdf)')
    parser.add_argument('--output-dir', '-o', type=str, default='./LeetCode',
                        help='Output directory (default: ./LeetCode)')
    parser.add_argument('--no-headless', action='store_true',
                        help='Show browser window')
    
    args = parser.parse_args()
    
    # Create scraper
    scraper = LeetCodeScraper(
        category=args.difficulty,
        headless=not args.no_headless,
        output_dir=args.output_dir
    )
    
    try:
        # Get problems
        problems = scraper.get_problems(args.count)
        
        if not problems:
            logger.warning("No problems found")
            return
        
        # Process each problem
        for name, url in problems.items():
            problem = scraper.get_description(url, name)
            if problem:
                if args.format in ['pdf', 'both']:
                    scraper.to_pdf(problem)
                if args.format in ['md', 'both']:
                    scraper.to_markdown(problem)
        
        logger.info(f"Successfully scraped {len(problems)} problems")
        
    finally:
        scraper.close()


if __name__ == '__main__':
    main()
