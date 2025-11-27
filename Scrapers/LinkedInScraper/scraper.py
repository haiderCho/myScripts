#!/usr/bin/env python3
"""
LinkedIn Profile Scraper - Main Entry Point
Upgraded version with Selenium, authentication, and stealth mode
"""
import sys
import logging
from linkedin_scraper import LinkedInScraper
from utils import read_urls_from_file, export_data, create_progress_bar
from config import Config

def main():
    """Main function to run the LinkedIn scraper"""
    
    print("=" * 60)
    print("LinkedIn Profile Scraper - Upgraded Version")
    print("=" * 60)
    
    # Load configuration
    try:
        Config.validate()
        print("\n✓ Configuration loaded successfully")
        print("\nSettings:")
        for key, value in Config.display().items():
            print(f"  • {key}: {value}")
    except ValueError as e:
        print(f"\n❌ Configuration Error: {str(e)}")
        print("\nPlease follow these steps:")
        print("  1. Copy .env.example to .env")
        print("  2. Fill in your LinkedIn credentials")
        print("  3. Run the scraper again")
        return 1
    
    # Read URLs from file
    print("\n" + "-" * 60)
    try:
        urls = read_urls_from_file("links.txt")
        print(f"✓ Loaded {len(urls)} valid LinkedIn profile URLs from links.txt")
        
        if not urls:
            print("\n❌ No valid URLs found in links.txt")
            print("\nPlease add LinkedIn profile URLs (one per line) to links.txt")
            print("Example: https://www.linkedin.com/in/username/")
            return 1
            
    except FileNotFoundError:
        print("\n❌ File 'links.txt' not found!")
        print("\nPlease create a links.txt file with LinkedIn profile URLs")
        print("Example format:")
        print("  https://www.linkedin.com/in/username1/")
        print("  https://www.linkedin.com/in/username2/")
        return 1
    except Exception as e:
        print(f"\n❌ Error reading URLs: {str(e)}")
        return 1
    
    # Initialize and run scraper
    print("\n" + "-" * 60)
    print("Starting LinkedIn Scraper...")
    print("-" * 60 + "\n")
    
    try:
        # Use context manager for automatic cleanup
        with LinkedInScraper() as scraper:
            # Scrape all profiles
            results = scraper.scrape_profiles(urls)
            
            # Export results
            print("\n" + "-" * 60)
            print("Exporting results...")
            
            output_file = export_data(
                results, 
                Config.OUTPUT_FILENAME, 
                Config.EXPORT_FORMAT
            )
            
            print(f"✓ Data saved to: {output_file}")
            
            # Summary
            print("\n" + "=" * 60)
            print("SCRAPING COMPLETE!")
            print("=" * 60)
            
            successful = sum(1 for r in results if "Error" not in r)
            failed = len(results) - successful
            
            print(f"\nTotal Profiles: {len(results)}")
            print(f"  ✓ Successful: {successful}")
            if failed > 0:
                print(f"  ✗ Failed: {failed}")
            
            print(f"\nOutput: {output_file}")
            print(f"Log file: {Config.LOG_FILE}")
            print("\n" + "=" * 60)
            
            return 0
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Scraping interrupted by user")
        return 1
    except Exception as e:
        print(f"\n\n❌ Fatal error: {str(e)}")
        logging.exception("Fatal error occurred")
        return 1

if __name__ == "__main__":
    sys.exit(main())
