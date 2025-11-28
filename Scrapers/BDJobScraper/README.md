# BDJobs.com Job Scraper

Scrapes job postings from bdjobs.com (Bangladesh's largest job portal) with advanced filtering and export options.

## Features

- **Search by Keywords**: Find jobs by title, skills, or keywords
- **Location Filtering**: Filter jobs by location (e.g., Dhaka, Chittagong)
- **Pagination Support**: Automatically scrapes multiple pages
- **Retry Logic**: Handles network errors with exponential backoff
- **Rate Limiting**: Prevents blocking with request delays
- **Multiple Export Formats**: CSV, JSON, or both
- **Comprehensive Logging**: Track scraping progress and errors

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage
```bash
python JobScraper.py --keyword "software engineer" --limit 20
```

### Advanced Examples
```bash
# Search with location filter
python JobScraper.py --keyword "data analyst" --location "Dhaka" --limit 50

# Export to both CSV and JSON
python JobScraper.py -k "manager" --limit 30 --format both

# Custom output filename
python JobScraper.py -k "developer" -l "Chittagong" -o jobs_output --format json
```

## CLI Arguments

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| `--keyword` | `-k` | Job keyword (required) | - |
| `--location` | `-l` | Job location | "" |
| `--category` | `-c` | Job category | "" |
| `--limit` | `-n` | Number of jobs | 20 |
| `--output` | `-o` | Output filename | bdjobs_output |
| `--format` | `-f` | Format (csv/json/both) | csv |

## Output Format

**CSV Columns**: title, company, location, education, experience, deadline, url

**JSON Structure**:
```json
[
  {
    "title": "Software Engineer",
    "company": "Tech Company Ltd.",
    "location": "Dhaka",
    "education": "Bachelor's Degree",
    "experience": "2-3 years",
    "deadline": "31 Dec 2025",
    "url": "https://jobs.bdjobs.com/..."
  }
]
```

## Notes

- Respects rate limits to avoid being blocked
- Network errors are automatically retried
- Requires active internet connection
