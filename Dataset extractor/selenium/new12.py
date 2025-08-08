import json
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import requests

# Configuration
URL = "https://www.kseebsolutions.com/kseeb-sslc-class-10-science-solutions-chapter-1/"
OUTPUT_JSON = "qa_dataset.json"
USE_SELENIUM = False  # Disable Selenium if ChromeDriver fails (fallback to requests)
CHROME_DRIVER_PATH = "./chromedriver"  # Path to ChromeDriver (adjust for OS)

def scrape_with_requests(url):
    """Scrape static HTML using requests."""
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

def scrape_with_selenium(url):
    """Scrape dynamic content using Selenium."""
    try:
        service = Service(executable_path=CHROME_DRIVER_PATH)
        driver = webdriver.Chrome(service=service)
        driver.get(url)
        time.sleep(3)  # Wait for JavaScript
        html = driver.page_source
        driver.quit()
        return html
    except Exception as e:
        print(f"Selenium failed: {e}")
        return None

def extract_qa_pairs(html):
    """Extract Q&A pairs using regex pattern matching."""
    qa_pairs = []
    
    # Updated regex pattern to match your screenshot's format
    pattern = re.compile(
        r'Question\s*\d+\.\n(.+?)\nAnswer:\n(.+?)(?=\nQuestion|\Z)', 
        re.DOTALL
    )
    
    matches = pattern.finditer(html)
    for match in matches:
        question = match.group(1).strip()
        answer = match.group(2).strip()
        
        # Clean up answer formatting
        answer = re.sub(r'\n\s*', ' ', answer)  # Remove newlines and extra spaces
        answer = re.sub(r'\s+', ' ', answer)    # Collapse multiple spaces
        
        qa_pairs.append({
            "question": question,
            "answer": answer
        })
    
    return qa_pairs

def save_to_json(data, filename):
    """Save data to JSON."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved to {filename}")

if __name__ == "__main__":
    # Step 1: Fetch HTML
    html = scrape_with_selenium(URL) if USE_SELENIUM else scrape_with_requests(URL)
    if not html:
        exit("Failed to fetch HTML. Check URL or try USE_SELENIUM=True.")

    # Step 2: Extract Q&A
    qa_pairs = extract_qa_pairs(html)
    if not qa_pairs:
        exit("No Q&A pairs found. Adjust HTML parsing logic.")

    # Step 3: Save to JSON
    save_to_json(qa_pairs, OUTPUT_JSON)