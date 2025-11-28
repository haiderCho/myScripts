#!/usr/bin/env python3
"""
IMDB Movie Scraper
Author: haiderCho
Description: Scrapes movie information from IMDB with multiple export formats
"""

import requests
from bs4 import BeautifulSoup as bs
import argparse
import json
import csv
import time
import logging
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Base URLs
BASE_ID = "https://www.imdb.com/title"
BASE = "https://www.imdb.com/find?s=tt&q="


class IMDBScraper:
    """Scraper for IMDB movie information"""
    
    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries
        self.movies = []
    
    def _make_request(self, url: str, retry_count: int = 0) -> Optional[requests.Response]:
        """Make HTTP request with retry logic"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            if retry_count < self.max_retries:
                logger.warning(f"Request failed, retrying... ({retry_count + 1}/{self.max_retries})")
                time.sleep(2 ** retry_count)
                return self._make_request(url, retry_count + 1)
            else:
                logger.error(f"Request failed after {self.max_retries} retries: {e}")
                return None
    
    def get_info(self, soup) -> Optional[Dict]:
        """Extract movie information from soup"""
        info = {}
        
        try:
            # Title
            title_wrapper = soup.find('div', attrs={"class": "title_wrapper"})
            if title_wrapper and title_wrapper.h1:
                info["title"] = title_wrapper.h1.get_text(strip=True)
            
            # Year
            year_elem = soup.find('span', attrs={"id": "titleYear"})
            if year_elem and year_elem.a:
                info["year"] = year_elem.a.get_text(strip=True)
            
            # Rating
            rating_elem = soup.find('span', attrs={"itemprop": "ratingValue"})
            if rating_elem:
                info["rating"] = rating_elem.get_text(strip=True)
            
            # Genre
            subtext = soup.find("div", attrs={"class": "subtext"})
            if subtext and subtext.a:
                info["genre"] = subtext.a.get_text(strip=True)
            
            # Plot
            article = soup.find('div', attrs={"id": "titleStoryLine"})
            if article:
                plot_elem = article.find('div', attrs={"class": "canwrap"})
                if plot_elem and plot_elem.p and plot_elem.p.span:
                    info["plot"] = plot_elem.p.span.get_text(strip=True)
            
            # Details
            details = soup.find('div', attrs={"id": "titleDetails"})
            if details:
                blocks = details.findAll('div', attrs={"class": "txt-block"})
                for block in blocks:
                    if not block.h4:
                        continue
                    
                    heading = block.h4.get_text(strip=True)
                    
                    if heading == "Release Date:":
                        info["date"] = block.get_text(strip=True).replace("See more»", '').replace(heading, '')
                    elif heading == "Country:":
                        if block.a:
                            info["country"] = block.a.get_text(strip=True)
                    elif heading == "Language:":
                        if block.a:
                            info["language"] = block.a.get_text(strip=True)
                    elif heading == "Budget:":
                        info["budget"] = block.get_text(strip=True).replace(heading, '')
                    elif heading == "Cumulative Worldwide Gross:":
                        info["gross"] = block.get_text(strip=True).replace(heading, '')
                    elif heading == "Gross USA:":
                        info["gross_usa"] = block.get_text(strip=True).replace(heading, '')
                    elif heading == "Opening Weekend USA:":
                        info["opening_week_usa"] = block.get_text(strip=True).replace(heading, '')
            
            return info if len(info) > 2 else None
            
        except Exception as e:
            logger.warning(f"Error extracting movie info: {e}")
            return None
    
    def find_movies(self, query: str, limit: int = 5) -> List[Dict]:
        """Find and scrape movies matching query"""
        url = BASE + query
        response = self._make_request(url)
        
        if not response:
            return []
        
        soup = bs(response.text, 'lxml')
        movie_list = soup.findAll("tr", attrs={"class": "findResult"})[0:limit]
        
        if not movie_list:
            logger.warning("No results found")
            return []
        
        logger.info(f"Found {len(movie_list)} movies")
        
        for idx, movie in enumerate(movie_list):
            try:
                # Extract title ID
                result_text = movie.find('td', attrs={"class": "result_text"})
                if not result_text or not result_text.a:
                    continue
                
                title_id = result_text.a.attrs["href"][6:]
                movie_url = BASE_ID + title_id
                
                logger.info(f"Scraping movie {idx + 1}/{len(movie_list)}")
                
                # Get movie details
                resp = self._make_request(movie_url)
                if resp:
                    movie_soup = bs(resp.text, 'lxml')
                    info = self.get_info(movie_soup)
                    if info:
                        info['url'] = movie_url
                        self.movies.append(info)
                
                time.sleep(0.5)  # Rate limiting
                
            except Exception as e:
                logger.warning(f"Error processing movie {idx}: {e}")
        
        return self.movies
    
    def save_to_json(self, filename: str):
        """Save movies to JSON file"""
        if not self.movies:
            logger.warning("No movies to save")
            return
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.movies, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved {len(self.movies)} movies to {filename}")
        except Exception as e:
            logger.error(f"Error saving JSON: {e}")
    
    def save_to_csv(self, filename: str):
        """Save movies to CSV file"""
        if not self.movies:
            logger.warning("No movies to save")
            return
        
        try:
            # Get all possible fields
            all_fields = set()
            for movie in self.movies:
                all_fields.update(movie.keys())
            
            headers = sorted(all_fields)
            
            with open(filename, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                writer.writerows(self.movies)
            logger.info(f"Saved {len(self.movies)} movies to {filename}")
        except Exception as e:
            logger.error(f"Error saving CSV: {e}")


def main():
    parser = argparse.ArgumentParser(
        description='Scrape movie information from IMDB',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python IMDBScraper.py --title "Inception"
  python IMDBScraper.py -t "The Matrix" --limit 3 --format json
  python IMDBScraper.py -t "Interstellar" -o movies.csv
        """
    )
    
    parser.add_argument('--title', '-t', type=str, required=True,
                        help='Movie title to search for')
    parser.add_argument('--limit', '-l', type=int, default=5,
                        help='Number of top results to scrape (default: 5)')
    parser.add_argument('--output', '-o', type=str, default='imdb_output',
                        help='Output filename without extension (default: imdb_output)')
    parser.add_argument('--format', '-f', type=str, choices=['json', 'csv', 'both', 'console'],
                        default='console', help='Output format (default: console)')
    
    args = parser.parse_args()
    
    # Create scraper
    scraper = IMDBScraper()
    
    # Scrape movies
    movies = scraper.find_movies(args.title, args.limit)
    
    if not movies:
        logger.warning("No movies found")
        return
    
    # Output based on format
    if args.format == 'console':
        for movie in movies:
            print(json.dumps(movie, indent=2))
            print("\n" + "="*50 + "\n")
    
    if args.format in ['json', 'both']:
        scraper.save_to_json(f"{args.output}.json")
    
    if args.format in ['csv', 'both']:
        scraper.save_to_csv(f"{args.output}.csv")


if __name__ == "__main__":
    main()
