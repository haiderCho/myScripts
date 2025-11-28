"""
Test script to verify the scraper works correctly.
Scrapes only the first few pages of a course to test functionality.
"""

import os
import sys
from pathlib import Path
from bs4 import BeautifulSoup

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from w3schoolsScraper import W3SchoolsScraper


class TestScraper(W3SchoolsScraper):
    """Modified scraper that only scrapes first few pages for testing."""
    
    def scrape_course(self, course_key=None, max_pages=3):
        """Scrape only first few pages of a course for testing."""
        if course_key:
            self.course_name = course_key
        
        if not self.course_name or self.course_name not in self.courses:
            print("❌ Invalid course name!")
            print(f"\nAvailable courses: {', '.join(self.courses.keys())}")
            return
        
        course_config = self.courses[self.course_name]
        base_url = course_config['base_url']
        current_page = course_config['start_page']
        course_name = course_config['name']
        
        # Use test output directory
        course_dir = self.output_dir / f"{course_name}_TEST"
        
        print(f"\n{'='*60}")
        print(f"🧪 TESTING: Scraping first {max_pages} pages of {course_name}")
        print(f"{'='*60}\n")
        print(f"📁 Output directory: {course_dir.absolute()}\n")
        
        page_count = 0
        
        from urllib.parse import urljoin
        
        while current_page and page_count < max_pages:
            # Build full URL
            full_url = urljoin(base_url, current_page)
            page_count += 1
            
            print(f"[{page_count}/{max_pages}] 📄 {full_url}")
            
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
            print(f"     📝 Size: {len(markdown)} characters\n")
            
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
                import time
                time.sleep(0.3)  # Shorter delay for testing
            else:
                print("  ℹ️  No 'Next' button found")
                break
        
        # Create table of contents
        if self.scraped_pages:
            self.create_table_of_contents(course_dir)
        
        print(f"\n{'='*60}")
        print(f"✅ Test completed!")
        print(f"📊 Pages scraped: {page_count}")
        print(f"📁 Location: {course_dir.absolute()}")
        print(f"{'='*60}\n")
        
        return course_dir


if __name__ == "__main__":
    print("=" * 60)
    print("W3Schools Scraper - Test Mode")
    print("=" * 60)
    
    # Test with Python course (first 3 pages)
    scraper = TestScraper(course_name="python", output_dir="test_output")
    test_dir = scraper.scrape_course(max_pages=3)
    
    if test_dir and test_dir.exists():
        print("\n📂 Generated files:")
        for file in sorted(test_dir.glob("*.md")):
            size_kb = file.stat().st_size / 1024
            print(f"   • {file.name} ({size_kb:.1f} KB)")
        
        print("\n✨ Test successful! You can now use the main scraper:")
        print("   python w3schoolsScraper.py python")
    else:
        print("\n❌ Test failed - no files were generated")
