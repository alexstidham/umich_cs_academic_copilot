import requests
from bs4 import BeautifulSoup

# 1. The UMich 281 staff syllabus URL
url = "https://eecs281staff.github.io/eecs281.org/syllabus.html"

print(f"Fetching website data from {url}...")
response = requests.get(url)

# 2. Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# 3. Strip out the annoying HTML tags and just get raw text
raw_text = soup.get_text()

print("\n--- Successfully Read Website ---")
print(raw_text[:1000]) # Print the first 1000 characters
print("--------------------------------")
