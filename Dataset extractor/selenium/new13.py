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
USE_SELENIUM = True  # Enable since site likely uses JavaScript
CHROME_DRIVER_PATH = "./chromedriver"
DEBUG = True  # Set to True to see parsing details

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
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--disable-blink-features=AutomationControlled")
        
        service = Service(executable_path=CHROME_DRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)
        time.sleep(5)  # Increased wait time for JS rendering
        html = driver.page_source
        driver.quit()
        return html
    except Exception as e:
        print(f"Selenium failed: {e}")
        return None

def extract_qa_pairs(html):
    """Extract Q&A pairs using multiple methods."""
    qa_pairs = []
    
    # Method 1: Regex pattern matching (for clean text)
    pattern = re.compile(
        r'Question\s*\d+\.(.*?)Answer:(.*?)(?=Question\s*\d+\.|\Z)', 
        re.DOTALL
    )
    matches = pattern.finditer(html)
    for match in matches:
        question = match.group(1).strip()
        answer = match.group(2).strip()
        qa_pairs.append({"question": question, "answer": answer})
    
    if qa_pairs:
        if DEBUG: print(f"Found {len(qa_pairs)} Q&A pairs via regex")
        return qa_pairs
    
    # Method 2: HTML parsing (fallback)
    if DEBUG: print("Trying HTML parsing fallback...")
    soup = BeautifulSoup(html, 'html.parser')
    
    # Look for common question containers
    containers = soup.find_all(['div', 'section', 'article'], class_=re.compile(r'question|qa|entry-content'))
    
    for container in containers:
        # Try to find question and answer elements
        question = container.find(['h2', 'h3', 'h4', 'strong'])
        answer = container.find_next(['p', 'div', 'ol'])
        
        if question and answer:
            q_text = question.get_text(strip=True)
            a_text = answer.get_text(strip=True, separator=' ')
            
            # Basic validation
            if "question" in q_text.lower() and len(a_text) > 10:
                qa_pairs.append({
                    "question": q_text,
                    "answer": a_text
                })
    
    if DEBUG: 
        print(f"Found {len(qa_pairs)} Q&A pairs via HTML parsing")
        if not qa_pairs:
            print("Debug: Here's a sample of the HTML structure:")
            print(html[:2000])  # Print first 2000 chars for inspection
    
    return qa_pairs

def save_to_json(data, filename):
    """Save data to JSON."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(data)} Q&A pairs to {filename}")

if __name__ == "__main__":
    print("Starting scraping process...")
    
    # Step 1: Fetch HTML
    html = scrape_with_selenium(URL) if USE_SELENIUM else scrape_with_requests(URL)
    if not html:
        exit("Failed to fetch HTML content")
    
    # Step 2: Extract Q&A
    qa_pairs = extract_qa_pairs(html)
    if not qa_pairs:
        exit("No Q&A pairs found. Please check the DEBUG output above.")
    
    # Step 3: Save to JSON
    save_to_json(qa_pairs, OUTPUT_JSON)