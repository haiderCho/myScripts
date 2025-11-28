"""
W3Schools Course Scraper
Scrapes entire courses from W3Schools and saves them as markdown files for offline reading.

Usage:
    python w3schoolsScraper.py [course_name]
    
Examples:
    python w3schoolsScraper.py python
    python w3schoolsScraper.py javascript
    python w3schoolsScraper.py html
"""

import os
import json
import re
import time
from pathlib import Path
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import html2text


class W3SchoolsScraper:
    """Scrapes W3Schools courses and converts them to markdown files."""
    
    def __init__(self, course_name=None, output_dir="scraped_courses"):
        self.course_name = course_name
        self.output_dir = Path(output_dir)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Load course configuration
        self.courses = self._load_courses_config()
        
        # HTML to Markdown converter
        self.h2t = html2text.HTML2Text()
        self.h2t.ignore_links = False
        self.h2t.ignore_images = False
        self.h2t.ignore_emphasis = False
        self.h2t.body_width = 0  # Don't wrap lines
        self.h2t.single_line_break = False
        
        self.scraped_pages = []
        
    def _load_courses_config(self):
        """Load course configurations from JSON file or use defaults."""
        config_file = Path(__file__).parent / "courses_config.json"
        
        if config_file.exists():
            with open(config_file, 'r') as f:
                return json.load(f)
        else:
            # Default configuration
            return {
                "python": {
                    "base_url": "https://www.w3schools.com/python/",
                    "start_page": "python_intro.asp",
                    "stop_page": "python_ref_overview.asp",
                    "name": "Python"
                },
                "javascript": {
                    "base_url": "https://www.w3schools.com/js/",
                    "start_page": "js_intro.asp",
                    "stop_page": "js_versions.asp",
                    "name": "JavaScript"
                },
                "html": {
                    "base_url": "https://www.w3schools.com/html/",
                    "start_page": "html_intro.asp",
                    "stop_page": "html_examples.asp",
                    "name": "HTML"
                },
                "css": {
                    "base_url": "https://www.w3schools.com/css/",
                    "start_page": "css_intro.asp",
                    "stop_page": "css_examples.asp",
                    "name": "CSS"
                },
                "sql": {
                    "base_url": "https://www.w3schools.com/sql/",
                    "start_page": "sql_intro.asp",
                    "stop_page": "sql_ref_keywords.asp",
                    "name": "SQL"
                }
            }
    
    def get_page(self, url, retries=3):
        """Fetch a page with retry logic."""
        for attempt in range(retries):
            try:
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                return response.content
            except requests.RequestException as e:
                print(f"  ⚠️  Error fetching {url} (attempt {attempt + 1}/{retries}): {e}")
                if attempt < retries - 1:
                    time.sleep(2)
                else:
                    print(f"  ❌ Failed to fetch {url} after {retries} attempts")
                    return None
    
    def extract_content(self, soup):
        """Extract main content from the page."""
        # Target the main tutorial content container first
        main_content = soup.find('div', {'id': 'main'})
        
        if not main_content:
            return None
        
        # Now clean up unwanted elements within a copy of main_content
        # Convert to string and reparse to avoid modifying the original
        content_str = str(main_content)
        cleaned_soup = BeautifulSoup(content_str, 'html.parser')
        
        # Remove scripts, styles, and other non-content elements
        for element in cleaned_soup.find_all(['script', 'style', 'iframe', 'noscript']):
            element.decompose()
        
        # Remove navigation and UI elements by class patterns
        unwanted_class_patterns = [
            'nextprev', 'w3-clear', 'w3-panel', 
            'bottomad', 'ad-', 'adsbygoogle', 'sharethis',
            'login', 'signin'
        ]
        for pattern in unwanted_class_patterns:
            for elem in cleaned_soup.find_all(class_=lambda x: x and pattern in str(x).lower()):
                elem.decompose()
        
        # Remove unwanted divs by ID
        unwanted_ids = [
            'adngin-top_leaderboard-0', 'adngin-mid_content-0',
            'adngin-below_content-0', 'subscribe'
        ]
        for elem_id in unwanted_ids:
            for elem in cleaned_soup.find_all(id=elem_id):
                elem.decompose()
        
        # Remove buttons except "Try it Yourself"
        for elem in cleaned_soup.find_all('button'):
            if 'Try it Yourself' not in elem.get_text():
                elem.decompose()
        
        # Remove forms
        for elem in cleaned_soup.find_all('form'):
            elem.decompose()
        
        return cleaned_soup
    
    def get_title(self, soup):
        """Extract page title."""
        # Try h1 tag first
        h1 = soup.find('h1')
        if h1:
            return h1.get_text(strip=True)
        
        # Fallback to title tag
        title = soup.find('title')
        if title:
            return title.get_text(strip=True).replace('W3Schools', '').strip()
        
        return "Untitled"
    
    def get_next_url(self, soup, base_url):
        """Find the 'Next' button URL."""
        # Look for next navigation button
        next_link = soup.find('a', {'class': 'w3-right w3-btn'})
        if not next_link:
            # Alternative: look in navigation div
            nav_div = soup.find('div', {'class': 'w3-clear nextprev'})
            if nav_div:
                links = nav_div.find_all('a')
                for link in links:
                    if 'Next' in link.get_text() or '❯' in link.get_text():
                        next_link = link
                        break
        
        if next_link and next_link.get('href'):
            return next_link.get('href')
        
        return None
    
    def sanitize_filename(self, filename):
        """Create a valid filename from a string."""
        # Remove invalid characters
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        # Replace spaces and special chars with underscores
        filename = re.sub(r'[\s\-]+', '_', filename)
        # Limit length
        filename = filename[:100]
        return filename
    
    def convert_to_markdown(self, html_content, title):
        """Convert HTML content to markdown."""
        if not html_content:
            return f"# {title}\n\n*Content could not be extracted*\n"
        
        # Convert HTML to markdown
        markdown = self.h2t.handle(str(html_content))
        
        # Clean up markdown
        markdown = re.sub(r'\n{3,}', '\n\n', markdown)  # Remove excessive newlines
        markdown = re.sub(r'\[\s*\]\([^)]*\)', '', markdown)  # Remove empty links
        markdown = re.sub(r'^\s*×\s*$', '', markdown, flags=re.MULTILINE)  # Remove × symbols
        markdown = re.sub(r'\\' + r'\(', '(', markdown)  # Fix escaped parentheses
        markdown = re.sub(r'\\' + r'\)', ')', markdown)
        
        # Remove lines that are just underscores or dashes (often table separators from headers)
        markdown = re.sub(r'^[-_]{3,}\s*$', '', markdown, flags=re.MULTILINE)
        
        # Clean up multiple consecutive blank lines
        markdown = re.sub(r'\n{3,}', '\n\n', markdown)
        
        # Strip leading/trailing whitespace
        markdown = markdown.strip()
        
        # Add title at the top if it's not already there
        if not markdown.startswith(f"# {title}"):
            markdown = f"# {title}\n\n{markdown}"
        
        return markdown
    
    def save_markdown(self, content, filename, course_dir):
        """Save markdown content to a file."""
        course_dir.mkdir(parents=True, exist_ok=True)
        filepath = course_dir / f"{filename}.md"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filepath
    
    def create_table_of_contents(self, course_dir):
        """Create a table of contents markdown file."""
        toc_content = "# Table of Contents\n\n"
        
        for idx, page in enumerate(self.scraped_pages, 1):
            filename = page['filename']
            title = page['title']
            toc_content += f"{idx}. [{title}]({filename}.md)\n"
        
        toc_path = course_dir / "00_table_of_contents.md"
        with open(toc_path, 'w', encoding='utf-8') as f:
            f.write(toc_content)
        
        print(f"\n✅ Created table of contents: {toc_path}")
    
    def scrape_course(self, course_key=None):
        """Scrape an entire course."""
        if course_key:
            self.course_name = course_key
        
        if not self.course_name or self.course_name not in self.courses:
            print("❌ Invalid course name!")
            print(f"\nAvailable courses: {', '.join(self.courses.keys())}")
            return
        
        course_config = self.courses[self.course_name]
        base_url = course_config['base_url']
        current_page = course_config['start_page']
        stop_page = course_config.get('stop_page', '')
        course_name = course_config['name']
        
        course_dir = self.output_dir / course_name
        
        print(f"\n{'='*60}")
        print(f"🚀 Starting to scrape W3Schools {course_name} Course")
        print(f"{'='*60}\n")
        print(f"📁 Output directory: {course_dir.absolute()}\n")
        
        page_count = 0
        visited_pages = set()
        
        while current_page:
            # Avoid infinite loops
            if current_page in visited_pages:
                print(f"⚠️  Already visited {current_page}, stopping to avoid loop")
                break
            
            visited_pages.add(current_page)
            
            # Check if we've reached the stop page
            if stop_page and current_page == stop_page:
                print(f"🛑 Reached stop page: {stop_page}")
                break
            
            # Build full URL
            full_url = urljoin(base_url, current_page)
            page_count += 1
            
            print(f"[{page_count}] 📄 {full_url}")
            
            # Fetch the page
            html_content = self.get_page(full_url)
            if not html_content:
                print(f"  ⏭️  Skipping page due to fetch error")
                break
            
            # Parse HTML
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extract information
            title = self.get_title(soup)
            print(f"     Title: {title}")
            
            main_content = self.extract_content(soup)
            
            # Convert to markdown
            markdown = self.convert_to_markdown(main_content, title)
            
            # Create filename
            safe_title = self.sanitize_filename(title)
            filename = f"{page_count:02d}_{safe_title}"
            
            # Save file
            filepath = self.save_markdown(markdown, filename, course_dir)
            print(f"     ✅ Saved: {filepath.name}")
            
            # Track scraped page
            self.scraped_pages.append({
                'title': title,
                'filename': filename,
                'url': full_url
            })
            
            # Find next page
            next_url = self.get_next_url(soup, base_url)
            
            if next_url:
                current_page = next_url
                # Be nice to the server
                time.sleep(0.5)
            else:
                print("\n  ℹ️  No 'Next' button found, reached end of course")
                break
        
        # Create table of contents
        if self.scraped_pages:
            self.create_table_of_contents(course_dir)
        
        print(f"\n{'='*60}")
        print(f"✨ Scraping completed!")
        print(f"📊 Total pages scraped: {page_count}")
        print(f"📁 Location: {course_dir.absolute()}")
        print(f"{'='*60}\n")


def main():
    """Main entry point."""
    import sys
    
    # Parse command line arguments
    course_name = sys.argv[1].lower() if len(sys.argv) > 1 else None
    
    # Create scraper instance
    scraper = W3SchoolsScraper(course_name=course_name)
    
    # If no course specified, show available courses
    if not course_name:
        print("W3Schools Course Scraper")
        print("=" * 40)
        print("\nAvailable courses:")
        for key, config in scraper.courses.items():
            print(f"  • {key:12s} - {config['name']}")
        print("\nUsage:")
        print(f"  python {Path(__file__).name} <course_name>")
        print("\nExample:")
        print(f"  python {Path(__file__).name} python")
        return
    
    # Scrape the course
    scraper.scrape_course()


if __name__ == "__main__":
    main()
