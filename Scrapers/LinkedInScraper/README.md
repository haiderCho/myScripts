# LinkedIn Profile Scraper

A LinkedIn profile scraper using Selenium WebDriver with authentication, stealth mode, and robust error handling.

## ⚠️ Important Disclaimer

**Legal Notice:** Web scraping LinkedIn may violate their [Terms of Service](https://www.linkedin.com/legal/user-agreement). This tool is provided for **educational purposes only**. Use responsibly and at your own risk.

**Recommendations:**
- Only scrape your own profile or profiles you have permission to scrape
- Use for legitimate research purposes only
- Respect LinkedIn's rate limits and robots.txt
- Comply with applicable laws (GDPR, CCPA, etc.)

**Risks:**
- Account suspension or permanent ban
- IP blocking
- CAPTCHA challenges
- Legal action

## Features

✨ **Selenium WebDriver** - Handles JavaScript rendering
🔐 **Authentication** - Automated LinkedIn login
🥷 **Stealth Mode** - Avoids bot detection
⏱️ **Rate Limiting** - Random delays between requests
🔄 **Retry Logic** - Automatic retry with exponential backoff
📊 **Multiple Export Formats** - Excel, CSV, JSON
📝 **Comprehensive Logging** - Detailed logs for debugging
🎯 **Progress Tracking** - Real-time progress updates
🛡️ **Error Handling** - Graceful degradation on errors

## Installation

### Prerequisites

- Python 3.7 or higher
- Google Chrome or Firefox browser
- LinkedIn account

### Setup

1. **Clone or download the scraper files**

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure credentials:**
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your LinkedIn credentials
# Use a text editor to fill in your email and password
```

4. **Prepare URL list:**
Create a `links.txt` file with LinkedIn profile URLs (one per line):
```
https://www.linkedin.com/in/username1/
https://www.linkedin.com/in/username2/
https://www.linkedin.com/in/username3/
```

## Usage

### Basic Usage

```bash
python scraper.py
```

The scraper will:
1. Load configuration from `.env`
2. Read URLs from `links.txt`
3. Login to LinkedIn
4. Scrape each profile
5. Export data to the specified format

### Configuration Options

Edit `.env` to customize scraper behavior:

```env
# Required: LinkedIn Credentials
LINKEDIN_EMAIL=your.email@example.com
LINKEDIN_PASSWORD=your_password_here

# Optional: Scraper Settings
MIN_DELAY=3                      # Min delay between requests (seconds)
MAX_DELAY=7                      # Max delay between requests (seconds)
MAX_PROFILES_PER_SESSION=50      # Limit profiles per session

# Optional: Browser Settings
HEADLESS=False                   # Run browser in background (True/False)
BROWSER=chrome                   # Browser to use (chrome/firefox)

# Optional: Export Settings
EXPORT_FORMAT=excel              # Output format (excel/csv/json)
OUTPUT_FILENAME=scraped_output   # Output filename (without extension)

# Optional: Advanced Settings
PAGE_LOAD_TIMEOUT=30             # Page load timeout (seconds)
ELEMENT_WAIT_TIMEOUT=10          # Element wait timeout (seconds)
MAX_RETRIES=3                    # Max retry attempts
LOG_LEVEL=INFO                   # Logging level (DEBUG/INFO/WARNING/ERROR)
```

## Data Collected

The scraper extracts the following information from each profile:

- **URL** - LinkedIn profile URL
- **LinkedIn_ID** - Extracted profile ID
- **Name** - Full name
- **Headline** - Professional headline/title
- **Location** - Geographic location
- **About** - About/summary section
- **Current_Position** - Current job title
- **Current_Company** - Current employer
- **Education** - Most recent education
- **Connections** - Number of connections (if visible)

## Output Files

- **scraped_output.xlsx** (or .csv/.json) - Scraped data
- **linkedin_scraper.log** - Detailed log file

## Troubleshooting

### Login Issues

**Problem:** "Login failed" error

**Solutions:**
- Verify credentials in `.env` are correct
- Check if LinkedIn requires CAPTCHA (complete it manually in the browser)
- Try disabling 2FA temporarily
- Use headless=False to see what's happening

### CAPTCHA Challenges

**Problem:** LinkedIn shows CAPTCHA during login

**Solution:**
The scraper will detect CAPTCHA and pause for 5 minutes, allowing you to complete it manually in the browser window.

### Session Expiration

**Problem:** "Session expired" during scraping

**Solution:**
The scraper automatically re-authenticates if session expires.

### Rate Limiting

**Problem:** Account gets temporarily blocked

**Solutions:**
- Increase delay range (e.g., MIN_DELAY=5, MAX_DELAY=10)
- Reduce MAX_PROFILES_PER_SESSION
- Wait 24 hours before resuming

### Element Not Found

**Problem:** "Could not find name" or other warnings

**Causes:**
- LinkedIn changed their HTML structure
- Profile is private or restricted
- Network issues

**Solutions:**
- Update selectors in `linkedin_scraper.py`
- Check if profile is publicly accessible
- Review log file for details

## Best Practices

1. **Start Small:** Test with 2-3 profiles first
2. **Use Delays:** Keep delays at 3-7 seconds minimum
3. **Limit Volume:** Don't scrape more than 50 profiles per session
4. **Monitor Logs:** Check logs regularly for errors
5. **Respect Privacy:** Only scrape public information
6. **Rotate Accounts:** Don't use your main LinkedIn account

## Advanced Usage

### Custom Export Format

```python
from linkedin_scraper import LinkedInScraper
from utils import export_data

with LinkedInScraper() as scraper:
    results = scraper.scrape_profiles(urls)
    
    # Export to multiple formats
    export_data(results, "output", "excel")
    export_data(results, "output", "csv")
    export_data(results, "output", "json")
```

### Scrape Single Profile

```python
from linkedin_scraper import LinkedInScraper

with LinkedInScraper() as scraper:
    profile = scraper.scrape_profile("https://www.linkedin.com/in/username/")
    print(profile)
```

## Project Structure

```
Scrapers/
├── scraper.py              # Main entry point
├── linkedin_scraper.py     # Core scraper class
├── config.py               # Configuration management
├── utils.py                # Helper functions
├── requirements.txt        # Python dependencies
├── .env.example            # Example environment file
├── .env                    # Your credentials (gitignored)
├── .gitignore             # Git ignore rules
├── links.txt              # Input URLs
└── README.md              # This file
```

## Dependencies

- **selenium** - Browser automation
- **webdriver-manager** - Automatic WebDriver management
- **selenium-stealth** - Stealth mode to avoid detection
- **beautifulsoup4** - HTML parsing
- **pandas** - Data manipulation
- **openpyxl** - Excel file support
- **python-dotenv** - Environment variable management

## FAQ

**Q: Is this legal?**
A: Web scraping legality varies by jurisdiction and use case. LinkedIn's ToS prohibit automated scraping. Use at your own risk.

**Q: Will my account get banned?**
A: Possible, especially with aggressive scraping. Use conservative settings and limit volume.

**Q: Can I scrape without logging in?**
A: No, LinkedIn requires authentication to view most profile information.

**Q: How fast can I scrape?**
A: Recommended: 3-7 second delays, max 50 profiles per session. Faster = higher ban risk.

**Q: What if LinkedIn changes their website?**
A: You'll need to update the CSS selectors in `linkedin_scraper.py`.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review `linkedin_scraper.log` for details
3. Verify your configuration in `.env`

## License

This project is provided as-is for educational purposes only. Use responsibly and at your own risk.

---

**Remember:** Always respect LinkedIn's Terms of Service and applicable laws. This tool is for educational purposes only.
