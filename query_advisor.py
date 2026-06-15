import os
import chromadb
from dotenv import load_dotenv
from google import genai

# 1. Load Gemini API Key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# 2. Connect to our local ChromaDB database
chroma_client = chromadb.PersistentClient(path="./chroma_storage")
collection = chroma_client.get_collection(name="umich_academic_rules")

# 3. Define the Student's "Edge Case" Scenario
student_profile = """
I am a UMich CS major currently enrolled in EECS 281.
Due to unexpected personal reasons, I need to take the second half of the semester off
and withdraw temporarily. I plan to return next semester.
"""

student_question = "What is the policy for withdrawing or handling incompletes for this course?"

print("Step 1: Searching the Vector Database for relevant rules...")
# 4. Query ChromaDB. It automatically finds text chunks relevant to the question!
results = collection.query(
    query_texts=[student_question],
    n_results=5 # Grab the top 5 most relevant paragraphs
)

# Combine the retrieved database chunks into one string
retrieved_context = "\n".join(results['documents'][0])

print("Step 2: Sending the database facts + student profile to Gemini...")
# 5. Craft the Prompt using our dynamic architecture
orchestrator_prompt = f"""
You are an expert Academic Advisor for the University of Michigan Computer Science department.
Your job is to help students navigate complex scenarios using ONLY the official course data provided below.

STUDENT PROFILE & SITUATION:
{student_profile}

RELEVANT COURSE POLICY DATA (From Database):
{retrieved_context}

STUDENT QUESTION:
{student_question}

Provide a clear, empathetic, and highly accurate response outlining their options based strictly on the data.
"""

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=orchestrator_prompt,
)

print("\n--- 🤖 DYNAMIC ADVISOR RESPONSE ---")
print(response.text)
