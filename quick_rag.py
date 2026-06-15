import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from google import genai

# 1. Load your API Key safely
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# 2. Ingest the EECS 281 Syllabus from the web
url = "https://eecs281staff.github.io/eecs281.org/syllabus.html"
print("Fetching EECS 281 syllabus data from the web...")
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
syllabus_text = soup.get_text()

# 3. Formulate the student question (The Scenario)
student_scenario = """
I am an undergraduate student planning my semester. Based ONLY on the provided syllabus,
what is the policy regarding late submissions for projects, and what is the absolute
final deadline to turn something in late?
"""

# 4. Combine the Fact Sheet (Syllabus) + Question into the Prompt
full_prompt = f"""
Context / Syllabus Data:
{syllabus_text}

User Question:
{student_scenario}
"""

print("Sending 281 Syllabus + your question to Gemini...")
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=full_prompt,
)

print("\n--- 281 Advisor Bot Response ---")
print(response.text)
