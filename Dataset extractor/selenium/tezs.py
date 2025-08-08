# import json
# import re
# import time
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from bs4 import BeautifulSoup
# import requests

# # Configuration
# URL = "https://www.kseebsolutions.com/kseeb-sslc-class-10-science-solutions-chapter-1/"  # Replace with your target URL
# OUTPUT_JSON = "qa_dataset.json"
# USE_SELENIUM = True  # Set to False if the page is static
# CHROME_DRIVER_PATH = "chromedriver.exe"  # Replace with your path

# def scrape_with_requests(url):
#     """Scrape static HTML content using requests."""
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
#     }
#     try:
#         response = requests.get(url, headers=headers)
#         response.raise_for_status()
#         return response.text
#     except requests.RequestException as e:
#         print(f"Request failed: {e}")
#         return None

# def scrape_with_selenium(url):
#     """Scrape dynamic content using Selenium."""
#     try:
#         service = Service(CHROME_DRIVER_PATH)
#         driver = webdriver.Chrome(service=service)
#         driver.get(url)
#         time.sleep(3)  # Wait for JavaScript to load
#         html = driver.page_source
#         driver.quit()
#         return html
#     except Exception as e:
#         print(f"Selenium failed: {e}")
#         return None

# def extract_qa_pairs(html):
#     """Extract Q&A pairs from HTML using heuristic rules."""
#     soup = BeautifulSoup(html, 'html.parser')
#     qa_pairs = []

#     # Heuristic 1: Questions in <h2>/<h3>, answers in next <p> or <div>
#     for question_tag in soup.find_all(['h2', 'h3']):
#         question = question_tag.get_text(strip=True)
#         answer_tag = question_tag.find_next(['p', 'div'])
#         answer = answer_tag.get_text(strip=True) if answer_tag else "N/A"
#         if question and answer:
#             qa_pairs.append({"question": question, "answer": answer})

#     # Heuristic 2: Q&A in alternating <div> pairs
#     containers = soup.find_all('div', class_=re.compile(r'question|answer', re.I))
#     for i in range(0, len(containers), 2):
#         if i + 1 < len(containers):
#             qa_pairs.append({
#                 "question": containers[i].get_text(strip=True),
#                 "answer": containers[i+1].get_text(strip=True)
#             })

#     return qa_pairs

# def save_to_json(data, filename):
#     """Save data to a JSON file."""
#     with open(filename, 'w', encoding='utf-8') as f:
#         json.dump(data, f, indent=2, ensure_ascii=False)
#     print(f"Data saved to {filename}")

# if __name__ == "__main__":
#     # Step 1: Fetch HTML
#     html = scrape_with_selenium(URL) if USE_SELENIUM else scrape_with_requests(URL)
#     if not html:
#         exit("Failed to fetch HTML")

#     # Step 2: Extract Q&A
#     qa_pairs = extract_qa_pairs(html)
#     if not qa_pairs:
#         exit("No Q&A pairs found. Adjust the extraction logic.")

#     # Step 3: Save to JSON
#     save_to_json(qa_pairs, OUTPUT_JSON)