# W3Schools Course Scraper

A comprehensive Python scraper that downloads entire W3Schools courses and saves them as clean markdown files for offline reading.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# View available courses
python w3schoolsScraper.py

# Scrape a course
python w3schoolsScraper.py python
```

## Features

- 🚀 **Automatic Course Navigation** - Follows "Next" links through entire courses
- 📝 **Markdown Export** - Clean, readable markdown format
- 📁 **Organized Output** - Creates course-specific directories with numbered files
- 📚 **Table of Contents** - Auto-generated ToC for easy navigation
- 🔄 **Multi-Course Support** - Pre-configured for 10+ popular courses
- ⚡ **Error Handling** - Retry logic and graceful error recovery
- 🎯 **Progress Tracking** - Real-time progress updates
- 🧹 **Clean Extraction** - Removes ads, navigation, and unnecessary elements

## Installation

1. Navigate to the scraper directory:
```bash
cd -\myScripts\Scrapers\w3schoolsScraper
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

**Dependencies:**
- `beautifulsoup4` - HTML parsing
- `requests` - HTTP requests
- `html2text` - HTML to Markdown conversion
- `lxml` - Fast XML/HTML processing

## Usage

### View Available Courses

```bash
python w3schoolsScraper.py
```

This will display all available courses:
- python
- javascript
- html
- css
- sql
- php
- java
- react
- bootstrap
- jquery

### Scrape a Course

```bash
python w3schoolsScraper.py <course_name>
```

**Examples:**

```bash
# Scrape Python course
python w3schoolsScraper.py python

# Scrape JavaScript course
python w3schoolsScraper.py javascript

# Scrape HTML course
python w3schoolsScraper.py html
```

## Output Structure

Scraped courses are saved in the `scraped_courses` directory:

```
scraped_courses/
├── Python/
│   ├── 00_table_of_contents.md
│   ├── 01_Python_Introduction.md
│   ├── 02_Python_Get_Started.md
│   ├── 03_Python_Syntax.md
│   └── ...
├── JavaScript/
│   ├── 00_table_of_contents.md
│   ├── 01_JavaScript_Introduction.md
│   └── ...
└── HTML/
    └── ...
```

✨ **Key Features:**
- Clean heading structure
- Properly formatted bullet points
- Code examples preserved with syntax
- No ads or navigation clutter
- Internal links maintained

## Testing

Before scraping a full course, test with the included test script:

```bash
# Test scraper with first 3 pages only
python test_scraper.py
```

This will create a `test_output/Python_TEST/` directory with sample pages to verify everything works correctly.

## Configuration

You can customize course settings in `courses_config.json`:

```json
{
  "course_name": {
    "base_url": "https://www.w3schools.com/course/",
    "start_page": "start.asp",
    "stop_page": "end.asp",
    "name": "Course Display Name",
    "description": "Course description"
  }
}
```

## Features in Detail

### Automatic Content Extraction
- Removes ads and navigation elements
- Preserves code examples with proper formatting
- Maintains heading hierarchy
- Converts HTML tables to markdown tables

### Error Handling
- 3 retry attempts for failed requests
- Graceful handling of missing content
- Detection and prevention of infinite loops

### Progress Tracking
- Real-time page count
- URL and title display for each page
- Success/error indicators

## Advanced Usage

### Adding New Courses

To add a new course not in the default configuration:

1. Open `courses_config.json`
2. Add a new entry following this format:

```json
{
  "new_course": {
    "base_url": "https://www.w3schools.com/new_course/",
    "start_page": "intro.asp",
    "stop_page": "examples.asp",
    "name": "New Course",
    "description": "Description of the course"
  }
}
```

3. Run: `python w3schoolsScraper.py new_course`

### Best Practices

**For Large Courses:**
- Start during off-peak hours
- Monitor the first 5-10 pages to ensure quality
- Check available disk space (some courses can be 50+ pages)

**For Better Organization:**
- Keep `scraped_courses` directory for all W3Schools content
- Use the table of contents files for quick navigation
- Consider organizing courses by programming language/topic

### Viewing Offline Content

**Recommended Markdown Viewers:**
- **VSCode**: Built-in preview (Ctrl+Shift+V)
- **Obsidian**: Great for building a knowledge base
- **Typora**: WYSIWYG markdown editor
- **Any text editor**: Plain text readable

**Tips:**
- Use VSCode workspace to open entire `scraped_courses` folder
- Enable markdown preview auto-refresh
- Use Ctrl+F for searching across all markdown files

## Notes

- The scraper includes a 0.5-second delay between requests to be respectful to W3Schools servers
- Some courses may have different stop pages; adjust in `courses_config.json` if needed
- Courses are periodically updated on W3Schools - you may want to re-scrape occasionally
- The scraper preserves "Try it Yourself" links which point to W3Schools online editor

## Troubleshooting

**Issue:** `ModuleNotFoundError: No module named 'bs4'` or similar  
**Solution:** Install dependencies with `pip install -r requirements.txt`

**Issue:** Course not scraping all pages  
**Solution:** 
- Check the `stop_page` setting in `courses_config.json`
- Some courses have different ending pages than expected
- Try adjusting the stop_page to include more content

**Issue:** Connection errors or timeouts  
**Solution:** 
- Check your internet connection
- Try again later (server might be busy)
- The scraper has built-in retry logic (3 attempts)

**Issue:** Generated markdown has weird formatting  
**Solution:**
- This is usually due to W3Schools page structure changes
- Report the issue with the course name
- The main content should still be readable

**Issue:** Scraper stops mid-course  
**Solution:**
- Check if you hit the stop_page
- Look for error messages in the console
- Resume by modifying the `start_page` in config to where it stopped

## FAQ

**Q: How long does it take to scrape a full course?**  
A: Depends on course size. Small courses (20-30 pages) take 15-30 seconds. Larger courses (100+ pages) can take 5-10 minutes due to the respectful delay between requests.

**Q: Can I scrape multiple courses at once?**  
A: It's better to do them one at a time to be respectful to W3Schools servers. You can run them sequentially in a batch script.

**Q: Will this work offline after scraping?**  
A: Yes! All content is saved locally. However, "Try it Yourself" links and some images may require internet.

**Q: Can I convert the markdown to PDF?**  
A: Yes! Use tools like Pandoc, Typora, or markdown-pdf converters. Example:
```bash
pandoc input.md -o output.pdf
```

**Q: Is this legal?**  
A: This is for personal, educational use only. W3Schools content is publicly available. Please respect their terms of service.

## License

Free to use for personal offline learning purposes. W3Schools content belongs to W3Schools.

---

**Happy Learning!** 📚✨

For issues or improvements, check the source code or modify the scraper to fit your needs.
