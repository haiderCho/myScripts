# Coursera Course Scraper

Scrapes course information from Coursera including titles, descriptions, reviews, and URLs.

## Features

- **Auto ChromeDriver**: Automatically downloads and manages ChromeDriver
- **Headless Mode**: Run without visible browser window
- **Multi-page Support**: Scrape multiple pages of results
- **Progress Logging**: Real-time scraping progress updates
- **Multiple Export Formats**: JSON, CSV, console, or both
- **Review Extraction**: Includes course ratings and reviews

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage
```bash
python CourseraScraper.py --keyword "python" --pages 3
```

### Advanced Examples
```bash
# Export to CSV
python CourseraScraper.py -k "machine learning" -p 5 --format csv

# Export to both JSON and CSV
python CourseraScraper.py -k "data science" --format both

# Show browser window (non-headless)
python CourseraScraper.py -k "web development" --no-headless

# Custom output filename
python CourseraScraper.py -k "AI" -p 2 -o my_courses --format json
```

## CLI Arguments

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| `--keyword` | `-k` | Search keyword (required) | - |
| `--pages` | `-p` | Number of pages | 1 |
| `--output` | `-o` | Output filename | coursera_output |
| `--format` | `-f` | Format (json/csv/both/console) | json |
| `--no-headless` | - | Show browser | False |

## Output Format

**CSV Columns**: id, title, description, review, url

**JSON Structure**:
```json
{
  "data": [
    {
      "id": 0,
      "title": "Python for Everybody",
      "description": "Learn to Program and Analyze Data with Python...",
      "review": "4.8⭐(500,000 ratings)",
      "url": "https://www.coursera.org/..."
    }
  ],
  "message": "Found 20 courses for 'python'"
}
```

## Requirements

- Chrome browser installed
- ChromeDriver (auto-installed via webdriver-manager)
