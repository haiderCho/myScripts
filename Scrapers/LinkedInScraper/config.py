"""
Configuration management for LinkedIn Scraper
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration settings for the LinkedIn scraper"""
    
    # LinkedIn Credentials
    LINKEDIN_EMAIL = os.getenv('LINKEDIN_EMAIL')
    LINKEDIN_PASSWORD = os.getenv('LINKEDIN_PASSWORD')
    
    # Scraper Settings
    MIN_DELAY = int(os.getenv('MIN_DELAY', '3'))  # Minimum delay between requests (seconds)
    MAX_DELAY = int(os.getenv('MAX_DELAY', '7'))  # Maximum delay between requests (seconds)
    MAX_PROFILES_PER_SESSION = int(os.getenv('MAX_PROFILES_PER_SESSION', '50'))
    
    # Browser Settings
    HEADLESS = os.getenv('HEADLESS', 'False').lower() == 'true'
    BROWSER = os.getenv('BROWSER', 'chrome').lower()  # chrome or firefox
    
    # Timeout Settings
    PAGE_LOAD_TIMEOUT = int(os.getenv('PAGE_LOAD_TIMEOUT', '30'))
    ELEMENT_WAIT_TIMEOUT = int(os.getenv('ELEMENT_WAIT_TIMEOUT', '10'))
    
    # Retry Settings
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))
    RETRY_DELAY = int(os.getenv('RETRY_DELAY', '5'))
    
    # Export Settings
    EXPORT_FORMAT = os.getenv('EXPORT_FORMAT', 'excel')  # excel, csv, or json
    OUTPUT_FILENAME = os.getenv('OUTPUT_FILENAME', 'scraped_output')
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'linkedin_scraper.log')
    
    @classmethod
    def validate(cls):
        """Validate that required configuration is present"""
        if not cls.LINKEDIN_EMAIL or not cls.LINKEDIN_PASSWORD:
            raise ValueError(
                "LinkedIn credentials not found! "
                "Please copy .env.example to .env and fill in your credentials."
            )
        
        if cls.MIN_DELAY > cls.MAX_DELAY:
            raise ValueError("MIN_DELAY cannot be greater than MAX_DELAY")
        
        if cls.BROWSER not in ['chrome', 'firefox']:
            raise ValueError("BROWSER must be either 'chrome' or 'firefox'")
        
        if cls.EXPORT_FORMAT not in ['excel', 'csv', 'json']:
            raise ValueError("EXPORT_FORMAT must be 'excel', 'csv', or 'json'")
        
        return True
    
    @classmethod
    def display(cls):
        """Display current configuration (without sensitive data)"""
        return {
            'Browser': cls.BROWSER,
            'Headless': cls.HEADLESS,
            'Delay Range': f'{cls.MIN_DELAY}-{cls.MAX_DELAY}s',
            'Max Profiles': cls.MAX_PROFILES_PER_SESSION,
            'Export Format': cls.EXPORT_FORMAT,
            'Log Level': cls.LOG_LEVEL
        }
