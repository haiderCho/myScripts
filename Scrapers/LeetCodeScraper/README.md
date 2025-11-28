# LeetCode Problem Scraper

Scrapes LeetCode coding problems with descriptions, test cases, and exports to PDF or Markdown.

## Features

- **Auto ChromeDriver**: Automatically downloads and manages ChromeDriver
- **Difficulty Filtering**: Easy, Medium, or Hard problems
- **Multiple Export Formats**: PDF, Markdown, or both
- **Headless Mode**: Run without visible browser window
- **Auto Directory Creation**: Creates output folder automatically
- **Complete Problem Data**: Title, statement, test cases, and problem URL
- **Modern Selenium**: Updated to latest Selenium 4 syntax

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage
```bash
python LeetCodeScraper.py --difficulty Easy --count 10
```

### Advanced Examples
```bash
# Scrape Medium problems to Markdown
python LeetCodeScraper.py -d Medium -n 5 --format md

# Export to both PDF and Markdown
python LeetCodeScraper.py -d Hard -n 3 --format both

# Custom output directory
python LeetCodeScraper.py -d Easy -n 20 -o ./MyProblems --format md

# Show browser window
python LeetCodeScraper.py -d Medium -n 5 --no-headless
```

## CLI Arguments

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| `--difficulty` | `-d` | Difficulty (Easy/Medium/Hard) | Easy |
| `--count` | `-n` | Number of problems | 5 |
| `--format` | `-f` | Format (pdf/md/both) | pdf |
| `--output-dir` | `-o` | Output directory | ./LeetCode |
| `--no-headless` | - | Show browser | False |

## Output Formats

### PDF
Professional PDF format with:
- Problem title (centered header)
- Problem statement
- Test cases
- Clickable problem URL

### Markdown
Clean Markdown format with:
```markdown
# Problem Title

## Problem Statement
[description]

## Test Cases
[code block with test cases]

## Link
[View on LeetCode](url)
```

## Requirements

- Chrome browser installed
- ChromeDriver (auto-installed via webdriver-manager)
- For PDF: fpdf library (included in requirements.txt)

## Notes

- Problems are saved as separate files in the output directory
- File names are based on problem titles
- Page loading uses "none" strategy for faster execution
- Some problems may fail to load due to LeetCode's dynamic content
