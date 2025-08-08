import requests
from bs4 import BeautifulSoup
import re
import json

# URL of the page you want to scrape
url = "https://www.kseebsolutions.com/kseeb-sslc-class-10-science-solutions-chapter-1/"

# Send a GET request to fetch the raw HTML content
response = requests.get(url)

# Check if the request was successful
if response.status_code != 200:
    print("Failed to retrieve the webpage.")
    exit()

print("Page successfully fetched!")

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Extract visible text from the page
text = soup.get_text(separator="\n")

# Clean up the text
text = re.sub(r'\n+', '\n', text)  # remove extra newlines
text = text.strip()

# Pattern: Question followed by number (e.g., "Question 1.") and "Answer:"
pattern = r'(Question\s+\d+\..*?)(?=Answer:)'  # match each question
question_matches = re.findall(pattern, text, re.DOTALL)

# Extract answers (each one starting with 'Answer:' up to next 'Question' or end of text)
answer_pattern = r'Answer:\s*(.*?)(?=Question\s+\d+\.|$)'  # match each answer
answer_matches = re.findall(answer_pattern, text, re.DOTALL)

# Clean and pair the results
qa_pairs = []
for q, a in zip(question_matches, answer_matches):
    qa_pairs.append({
        "question": q.strip().replace('\n', ' '),
        "answer": a.strip().replace('\n', ' ')
    })

# Save to JSON
with open('qa_data.json', 'w', encoding='utf-8') as f:
    json.dump(qa_pairs, f, indent=4, ensure_ascii=False)

print(f"Extracted {len(qa_pairs)} Q&A pairs and saved to qa_data.json.")
