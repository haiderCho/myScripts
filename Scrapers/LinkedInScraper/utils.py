"""
Utility functions for LinkedIn Scraper
"""
import re
import json
import pandas as pd
from datetime import datetime
from urllib.parse import urlparse

def is_valid_linkedin_url(url):
    """Validate if URL is a LinkedIn profile URL"""
    try:
        parsed = urlparse(url)
        return (
            parsed.scheme in ['http', 'https'] and
            'linkedin.com' in parsed.netloc and
            '/in/' in parsed.path
        )
    except Exception:
        return False

def clean_text(text):
    """Clean and normalize text data"""
    if not text:
        return None
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    # Remove special characters that might cause issues
    text = text.strip()
    
    return text if text else None

def extract_linkedin_id(url):
    """Extract LinkedIn profile ID from URL"""
    try:
        # Handle URLs like: https://www.linkedin.com/in/username/
        match = re.search(r'/in/([^/]+)/?', url)
        if match:
            return match.group(1)
    except Exception:
        pass
    return None

def format_timestamp():
    """Return current timestamp in readable format"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def save_to_excel(data, filename):
    """Save data to Excel file"""
    try:
        df = pd.DataFrame(data)
        output_file = f"{filename}.xlsx"
        df.to_excel(output_file, index=False, engine='openpyxl')
        return output_file
    except Exception as e:
        raise Exception(f"Failed to save Excel file: {str(e)}")

def save_to_csv(data, filename):
    """Save data to CSV file"""
    try:
        df = pd.DataFrame(data)
        output_file = f"{filename}.csv"
        df.to_csv(output_file, index=False, encoding='utf-8')
        return output_file
    except Exception as e:
        raise Exception(f"Failed to save CSV file: {str(e)}")

def save_to_json(data, filename):
    """Save data to JSON file"""
    try:
        output_file = f"{filename}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return output_file
    except Exception as e:
        raise Exception(f"Failed to save JSON file: {str(e)}")

def export_data(data, filename, format='excel'):
    """Export data in specified format"""
    if not data:
        raise ValueError("No data to export")
    
    format = format.lower()
    
    if format == 'excel':
        return save_to_excel(data, filename)
    elif format == 'csv':
        return save_to_csv(data, filename)
    elif format == 'json':
        return save_to_json(data, filename)
    else:
        raise ValueError(f"Unsupported format: {format}")

def read_urls_from_file(filepath):
    """Read URLs from text file and validate them"""
    urls = []
    invalid_urls = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                url = line.strip()
                if not url or url.startswith('#'):  # Skip empty lines and comments
                    continue
                
                if is_valid_linkedin_url(url):
                    urls.append(url)
                else:
                    invalid_urls.append((line_num, url))
        
        if invalid_urls:
            print(f"\n⚠️  Warning: Found {len(invalid_urls)} invalid URLs:")
            for line_num, url in invalid_urls[:5]:  # Show first 5
                print(f"   Line {line_num}: {url}")
            if len(invalid_urls) > 5:
                print(f"   ... and {len(invalid_urls) - 5} more")
        
        return urls
    
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filepath}")
    except Exception as e:
        raise Exception(f"Error reading file: {str(e)}")

def create_progress_bar(current, total, bar_length=50):
    """Create a simple text-based progress bar"""
    filled = int(bar_length * current / total)
    bar = '█' * filled + '░' * (bar_length - filled)
    percent = 100 * current / total
    return f"[{bar}] {percent:.1f}% ({current}/{total})"

def sanitize_filename(text, max_length=50):
    """Sanitize text for use in filenames"""
    if not text:
        return "unknown"
    
    # Remove invalid characters
    text = re.sub(r'[<>:"/\\|?*]', '', text)
    # Replace spaces with underscores
    text = text.replace(' ', '_')
    # Limit length
    if len(text) > max_length:
        text = text[:max_length]
    
    return text.lower()

def estimate_time(profiles_done, total_profiles, elapsed_seconds):
    """Estimate remaining time based on current progress"""
    if profiles_done == 0:
        return "Calculating..."
    
    avg_time_per_profile = elapsed_seconds / profiles_done
    remaining = total_profiles - profiles_done
    estimated_seconds = remaining * avg_time_per_profile
    
    if estimated_seconds < 60:
        return f"{int(estimated_seconds)}s"
    elif estimated_seconds < 3600:
        return f"{int(estimated_seconds / 60)}m {int(estimated_seconds % 60)}s"
    else:
        hours = int(estimated_seconds / 3600)
        minutes = int((estimated_seconds % 3600) / 60)
        return f"{hours}h {minutes}m"
