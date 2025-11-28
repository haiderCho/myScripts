# IMDB Movie Scraper

Scrapes detailed movie information from IMDB including ratings, plot, budget, and box office data.

## Features

- **Comprehensive Data**: Title, year, rating, genre, plot, budget, gross revenue
- **Multiple Results**: Search returns top 5 matching movies by default
- **Retry Logic**: Automatic retry on network failures
- **Multiple Export Formats**: JSON, CSV, console, or both
- **Flexible Search**: Searches across all IMDB entries
- **Detailed Information**: Release date, country, language, and more

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage
```bash
python IMDBScraper.py --title "Inception"
```

### Advanced Examples
```bash
# Limit results and export to JSON
python IMDBScraper.py -t "The Matrix" --limit 3 --format json

# Export to CSV
python IMDBScraper.py -t "Interstellar" --format csv

# Export to both formats with custom filename
python IMDBScraper.py -t "The Dark Knight" -l 5 -o movies --format both
```

## CLI Arguments

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| `--title` | `-t` | Movie title (required) | - |
| `--limit` | `-l` | Number of results | 5 |
| `--output` | `-o` | Output filename | imdb_output |
| `--format` | `-f` | Format (json/csv/both/console) | console |

## Output Format

**Available Fields**: title, year, rating, genre, plot, date, country, language, budget, gross, gross_usa, opening_week_usa, url

**JSON Structure**:
```json
[
  {
    "title": "Inception (2010)",
    "year": "2010",
    "rating": "8.8",
    "genre": "Action",
    "plot": "A thief who steals corporate secrets...",
    "country": "USA",
    "language": "English",
    "budget": "$160,000,000",
    "gross": "$836,848,102",
    "url": "https://www.imdb.com/title/tt1375666/"
  }
]
```

## Notes

- Not all movies have complete information (e.g., budget/gross may be missing)
- Top 5 results are scraped by default to ensure best match is included
- Network errors are automatically retried with exponential backoff
