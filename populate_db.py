import os
import requests
from bs4 import BeautifulSoup
import chromadb

print("Initializing local ChromaDB database...")
# 1. Set up Chroma to save data locally in a folder named 'chroma_storage'
chroma_client = chromadb.PersistentClient(path="./chroma_storage")

# 2. Create a "Collection" (think of this like a table in a database)
# If it already exists, we just grab it.
collection = chroma_client.get_or_create_collection(name="umich_academic_rules")

# 3. Scrape the EECS 281 Syllabus
url = "https://eecs281staff.github.io/eecs281.org/syllabus.html"
print("Scraping EECS 281 syllabus for database storage...")
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# 4. Clean up text and split it into separate paragraphs (chunks)
paragraphs = [p.get_text().strip() for p in soup.find_all(['p', 'h1', 'h2', 'h3', 'li'])]
chunks = [p for p in paragraphs if len(p) > 20] # Filter out empty/tiny lines

print(f"Split syllabus into {len(chunks)} individual semantic chunks.")

# 5. Add the chunks to our Vector Database
# ChromaDB handles converting these text strings into math vectors automatically under the hood!
documents = chunks
metadatas = [{"source": "EECS 281 Syllabus"} for _ in chunks]
ids = [f"eecs281_chunk_{i}" for i in range(len(chunks))]

print("Saving chunks into ChromaDB...")
collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids
)

print("\n Success! Your local vector database has been populated.")
print("You should now see a new 'chroma_storage' folder in your project directory.")
