import json
import os
import chromadb
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

try:
    with open("student_profile.json", "r") as f:
        student_profile = json.load(f)
except FileNotFoundError:
    print("❌ Error: 'student_profile.json' not found. Run onboard_student.py first!")
    exit()

chroma_client = chromadb.PersistentClient(path="./chroma_storage")
collection = chroma_client.get_collection(name="umich_academic_rules")

query_text = f"Prerequisites grading requirements and course sequencing for {student_profile['major']}"
print("Searching ChromaDB for relevant UMich CSE policy rules...")
db_results = collection.query(
    query_texts=[query_text],
    n_results=5
)
retrieved_policies = "\n".join(db_results['documents'][0])

# Format the course dictionary into a readable string for the prompt
courses_with_grades = "\n".join([f"- {course}: Grade {grade}" for course, grade in student_profile['completed_courses'].items()])

prompt = f"""
You are the official Academic Advisor for the University of Michigan Computer Science program.
Your task is to review a student's profile, enforce departmental rules, and generate a recommended plan for their upcoming term(s).

CRITICAL DEPARTMENTAL RULE TO ENFORCE:
- Students must earn a grade of 'C' or better in all pre-declaration, core EECS, and elective courses to satisfy CS degree requirements. Any grade of C- or below does NOT earn departmental credit and requires a retake before moving onto subsequent dependencies.

STUDENT PROFILE DATA:
- Major: {student_profile['major']}
- Next Semester: {student_profile['current_term']}
- Cumulative GPA: {student_profile['gpa']}
- Completed Courses & Grades:
{courses_with_grades}
- Student Constraints/Edge Cases: "{student_profile['constraints']}"

OFFICIAL COURSE DATA & POLICIES (From Vector DB):
{retrieved_policies}

OUTPUT FORMAT:
Provide an empathetic, professional advisor response. Include:
1. An analysis of their current standing (paying strict attention to any core course with a C- or lower that breaks prerequisite requirements).
2. A recommended course schedule for their next upcoming semester.
3. Next clear actionable steps for registration.
"""

print("Sending structured profile data and rules to Gemini...")
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=prompt,
)

print("\n================ 〽️ OFFICIAL UMICH CS ADVISING REPORT ================")
print(response.text)
print("=====================================================================")
