import os
from dotenv import load_dotenv
from google import genai

# 1. Load the API key from your .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# 2. Initialize the Gemini client
client = genai.Client(api_key=api_key)

# 3. Test the connection with a quick prompt
print("Sending message to Gemini...")
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents='Give me a 1-sentence hype cheer for a University of Michigan Computer Science student.',
)

print("\nGemini says:")
print(response.text)
