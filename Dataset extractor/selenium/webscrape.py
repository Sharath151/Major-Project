import requests
from bs4 import BeautifulSoup
import json

# URL of the page you want to scrape
url = "https://www.kseebsolutions.com/kseeb-sslc-class-10-science-solutions-chapter-1/"

# Send a GET request to fetch the raw HTML content
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    print("Page successfully fetched!")
else:
    print("Failed to retrieve the webpage.")
    exit()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find all question headings (h2 tags)
questions = soup.find_all('h2')

# Find all paragraphs (p tags) for answers
answers = soup.find_all('p')

# Create a list to hold the Q&A pairs
qa_pairs = []

# Loop through and create a dictionary for each Q&A pair
for i in range(min(len(questions), len(answers))):
    qa_pairs.append({
        'question': questions[i].get_text(strip=True),
        'answer': answers[i].get_text(strip=True)
    })

# Save to a JSON file
with open('qa_data.json', 'w') as json_file:
    json.dump(qa_pairs, json_file, indent=4)

print("Data saved to qa_data.json!")
