
import json
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import requests

# Configuration
URL = "https://www.kseebsolutions.com/kseeb-sslc-class-10-science-solutions-chapter-1/"  # Replace with your URL
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
        service = Service(executable_path=CHROME_DRIVER_PATH)  # Updated for Selenium 4
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
    """Extract Q&A pairs from HTML."""
    soup = BeautifulSoup(html, 'html.parser')
    qa_pairs = []
    
    # Heuristic: Questions in <h2>/<h3>, answers in next <p>
    for q_tag in soup.find_all(['h2', 'h3']):
        question = q_tag.get_text(strip=True)
        answer_tag = q_tag.find_next(['p', 'div'])
        answer = answer_tag.get_text(strip=True) if answer_tag else "N/A"
        if question and answer != "N/A":
            qa_pairs.append({"question": question, "answer": answer})
    
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