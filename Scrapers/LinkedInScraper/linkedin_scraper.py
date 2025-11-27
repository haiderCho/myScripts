"""
LinkedIn Profile Scraper with Selenium
Includes authentication, stealth mode, and robust error handling
"""
import time
import random
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

try:
    from selenium_stealth import stealth
    STEALTH_AVAILABLE = True
except ImportError:
    STEALTH_AVAILABLE = False
    logging.warning("selenium-stealth not available. Install it for better stealth capabilities.")

from config import Config
from utils import clean_text, extract_linkedin_id


class LinkedInScraper:
    """LinkedIn profile scraper with authentication and stealth capabilities"""
    
    def __init__(self):
        """Initialize the scraper with configuration"""
        Config.validate()
        self.driver = None
        self.is_logged_in = False
        self.profiles_scraped = 0
        self.setup_logging()
        
    def setup_logging(self):
        """Configure logging"""
        logging.basicConfig(
            level=getattr(logging, Config.LOG_LEVEL),
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(Config.LOG_FILE),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_driver(self):
        """Setup Selenium WebDriver with stealth options"""
        self.logger.info(f"Setting up {Config.BROWSER} WebDriver...")
        
        try:
            if Config.BROWSER == 'chrome':
                options = webdriver.ChromeOptions()
                
                # Stealth options
                options.add_argument('--disable-blink-features=AutomationControlled')
                options.add_experimental_option("excludeSwitches", ["enable-automation"])
                options.add_experimental_option('useAutomationExtension', False)
                
                # Performance options
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--disable-gpu')
                
                # Privacy options
                options.add_argument('--disable-web-security')
                options.add_argument('--allow-running-insecure-content')
                
                if Config.HEADLESS:
                    options.add_argument('--headless=new')
                    options.add_argument('--window-size=1920,1080')
                
                # User agent
                options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
                
                service = ChromeService(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=options)
                
                # Apply selenium-stealth if available
                if STEALTH_AVAILABLE:
                    stealth(self.driver,
                        languages=["en-US", "en"],
                        vendor="Google Inc.",
                        platform="Win32",
                        webgl_vendor="Intel Inc.",
                        renderer="Intel Iris OpenGL Engine",
                        fix_hairline=True,
                    )
                
            elif Config.BROWSER == 'firefox':
                options = webdriver.FirefoxOptions()
                
                if Config.HEADLESS:
                    options.add_argument('--headless')
                
                options.set_preference("general.useragent.override", 
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0")
                
                service = FirefoxService(GeckoDriverManager().install())
                self.driver = webdriver.Firefox(service=service, options=options)
            
            # Set timeouts
            self.driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
            self.driver.implicitly_wait(Config.ELEMENT_WAIT_TIMEOUT)
            
            self.logger.info("✓ WebDriver setup complete")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to setup WebDriver: {str(e)}")
            raise
    
    def login(self):
        """Login to LinkedIn"""
        if self.is_logged_in:
            self.logger.info("Already logged in")
            return True
        
        self.logger.info("Logging in to LinkedIn...")
        
        try:
            self.driver.get('https://www.linkedin.com/login')
            time.sleep(random.uniform(2, 4))
            
            # Enter email
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            email_field.clear()
            email_field.send_keys(Config.LINKEDIN_EMAIL)
            time.sleep(random.uniform(0.5, 1.5))
            
            # Enter password
            password_field = self.driver.find_element(By.ID, "password")
            password_field.clear()
            password_field.send_keys(Config.LINKEDIN_PASSWORD)
            time.sleep(random.uniform(0.5, 1.5))
            
            # Click login button
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            # Wait for login to complete
            time.sleep(random.uniform(3, 5))
            
            # Check if login was successful
            if "feed" in self.driver.current_url or "mynetwork" in self.driver.current_url:
                self.is_logged_in = True
                self.logger.info("✓ Successfully logged in")
                return True
            
            # Check for CAPTCHA or verification
            if "checkpoint" in self.driver.current_url or "challenge" in self.driver.current_url:
                self.logger.warning("⚠️  CAPTCHA or verification required!")
                self.logger.warning("Please complete the verification in the browser window")
                
                # Wait for user to complete verification (up to 5 minutes)
                for i in range(60):
                    time.sleep(5)
                    if "feed" in self.driver.current_url or "mynetwork" in self.driver.current_url:
                        self.is_logged_in = True
                        self.logger.info("✓ Verification completed, logged in")
                        return True
                
                self.logger.error("Verification timeout")
                return False
            
            self.logger.error("Login failed - unexpected page")
            return False
            
        except Exception as e:
            self.logger.error(f"Login failed: {str(e)}")
            return False
    
    def random_delay(self):
        """Add random delay between requests"""
        delay = random.uniform(Config.MIN_DELAY, Config.MAX_DELAY)
        self.logger.debug(f"Waiting {delay:.2f} seconds...")
        time.sleep(delay)
    
    def scrape_profile(self, url, retry_count=0):
        """Scrape a single LinkedIn profile"""
        
        if retry_count >= Config.MAX_RETRIES:
            self.logger.error(f"Max retries reached for {url}")
            return {"URL": url, "Error": "Max retries exceeded"}
        
        try:
            self.logger.info(f"Scraping profile: {url}")
            self.driver.get(url)
            time.sleep(random.uniform(2, 4))
            
            # Check if we're still logged in
            if "authwall" in self.driver.current_url or "login" in self.driver.current_url:
                self.logger.warning("Session expired, re-logging in...")
                self.is_logged_in = False
                if not self.login():
                    return {"URL": url, "Error": "Login failed"}
                return self.scrape_profile(url, retry_count + 1)
            
            # Initialize data dictionary
            profile_data = {"URL": url, "LinkedIn_ID": extract_linkedin_id(url)}
            
            # Scrape profile information
            try:
                # Name
                name_elem = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "h1.text-heading-xlarge"))
                )
                profile_data["Name"] = clean_text(name_elem.text)
            except:
                self.logger.warning("Could not find name")
                profile_data["Name"] = None
            
            # Headline/Title
            try:
                headline_elem = self.driver.find_element(By.CSS_SELECTOR, "div.text-body-medium")
                profile_data["Headline"] = clean_text(headline_elem.text)
            except:
                profile_data["Headline"] = None
            
            # Location
            try:
                location_elem = self.driver.find_element(By.CSS_SELECTOR, "span.text-body-small.inline.t-black--light.break-words")
                profile_data["Location"] = clean_text(location_elem.text)
            except:
                profile_data["Location"] = None
            
            # About section
            try:
                about_button = self.driver.find_element(By.XPATH, "//button[@aria-label='Show all About content']")
                about_button.click()
                time.sleep(1)
                
                about_elem = self.driver.find_element(By.CSS_SELECTOR, "div.display-flex.ph5.pv3")
                profile_data["About"] = clean_text(about_elem.text)
            except:
                try:
                    about_elem = self.driver.find_element(By.CSS_SELECTOR, "div.pv-about__summary-text")
                    profile_data["About"] = clean_text(about_elem.text)
                except:
                    profile_data["About"] = None
            
            # Current position/company
            try:
                experience_section = self.driver.find_element(By.ID, "experience")
                parent = experience_section.find_element(By.XPATH, "..")
                
                # Get first position
                first_position = parent.find_element(By.CSS_SELECTOR, "li.artdeco-list__item")
                
                position_title = first_position.find_element(By.CSS_SELECTOR, "span[aria-hidden='true']").text
                profile_data["Current_Position"] = clean_text(position_title)
                
                try:
                    company_name = first_position.find_element(By.CSS_SELECTOR, "span.t-14.t-normal span[aria-hidden='true']").text
                    profile_data["Current_Company"] = clean_text(company_name)
                except:
                    profile_data["Current_Company"] = None
                    
            except:
                profile_data["Current_Position"] = None
                profile_data["Current_Company"] = None
            
            # Education
            try:
                education_section = self.driver.find_element(By.ID, "education")
                parent = education_section.find_element(By.XPATH, "..")
                
                first_edu = parent.find_element(By.CSS_SELECTOR, "li.artdeco-list__item")
                school_name = first_edu.find_element(By.CSS_SELECTOR, "span[aria-hidden='true']").text
                profile_data["Education"] = clean_text(school_name)
            except:
                profile_data["Education"] = None
            
            # Connection count (if visible)
            try:
                connections_elem = self.driver.find_element(By.CSS_SELECTOR, "span.t-bold")
                connections_text = connections_elem.text
                if "connection" in connections_text.lower():
                    profile_data["Connections"] = clean_text(connections_text)
                else:
                    profile_data["Connections"] = None
            except:
                profile_data["Connections"] = None
            
            self.profiles_scraped += 1
            self.logger.info(f"✓ Successfully scraped profile: {profile_data.get('Name', 'Unknown')}")
            
            return profile_data
            
        except TimeoutException:
            self.logger.error(f"Timeout scraping {url}")
            time.sleep(Config.RETRY_DELAY)
            return self.scrape_profile(url, retry_count + 1)
            
        except Exception as e:
            self.logger.error(f"Error scraping {url}: {str(e)}")
            return {"URL": url, "Error": str(e)}
    
    def scrape_profiles(self, urls):
        """Scrape multiple LinkedIn profiles"""
        results = []
        total = len(urls)
        
        self.logger.info(f"Starting to scrape {total} profiles...")
        
        # Check session limit
        if total > Config.MAX_PROFILES_PER_SESSION:
            self.logger.warning(f"⚠️  Limiting to {Config.MAX_PROFILES_PER_SESSION} profiles per session")
            urls = urls[:Config.MAX_PROFILES_PER_SESSION]
        
        start_time = time.time()
        
        for idx, url in enumerate(urls, 1):
            self.logger.info(f"\n--- Profile {idx}/{len(urls)} ---")
            
            data = self.scrape_profile(url)
            results.append(data)
            
            # Random delay between profiles (except for last one)
            if idx < len(urls):
                self.random_delay()
            
            # Show progress
            elapsed = time.time() - start_time
            avg_time = elapsed / idx
            remaining = (len(urls) - idx) * avg_time
            self.logger.info(f"Progress: {idx}/{len(urls)} | Est. remaining: {remaining/60:.1f} min")
        
        self.logger.info(f"\n✓ Completed scraping {len(results)} profiles")
        return results
    
    def close(self):
        """Close the browser and cleanup"""
        if self.driver:
            self.logger.info("Closing browser...")
            self.driver.quit()
            self.driver = None
    
    def __enter__(self):
        """Context manager entry"""
        self.setup_driver()
        self.login()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
        return False
