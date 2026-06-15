import json
import os
import chromadb
from dotenv import load_dotenv
from google import genai
from google.genai import types
import curriculum_rules as rules

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

print("🧪 Starting Automated Academic Compliance Test Suite...")

# 1. Define hard edge-case matrix profiles to stress-test our AI logic
TEST_CASES = [
    {
        "name": "Scenario A: The Prerequisite Grade Trap (EECS 280 C-)",
        "major": "Computer Science",
        "current_term": "Fall 2026",
        "gpa": 2.7,
        "completed_courses": {"EECS 183": "A", "MATH 115": "B+", "EECS 280": "C-"},
        "constraints": "I want to take EECS 281 next semester.",
        "must_contain_keyword": "retake" # The AI must order a retake of 280
    },
    {
        "name": "Scenario B: The Strict Sequence Gatekeeper (Missing 281)",
        "major": "Computer Science",
        "current_term": "Winter 2027",
        "gpa": 3.6,
        "completed_courses": {"EECS 183": "A", "EECS 280": "A", "EECS 203": "A"},
        "constraints": "Can I skip 281 and go straight into Operating Systems EECS 482?",
        "must_contain_keyword": "cannot" # The AI must deny entry to 482
    },
    {
        "name": "Scenario C: Perfect Path Forward",
        "major": "Computer Science",
        "current_term": "Fall 2026",
        "gpa": 3.9,
        "completed_courses": {"EECS 183": "A", "EECS 280": "A", "EECS 203": "A", "EECS 281": "A-", "EECS 370": "B+"},
        "constraints": "Ready for high-level systems classes.",
        "must_contain_keyword": "482" # Should successfully recommend EECS 482 since prereqs are clear
    }
]

# 2. Establish connection to our knowledge base
chroma_client = chromadb.PersistentClient(path="./chroma_storage")
collection = chroma_client.get_collection(name="umich_academic_rules")

def run_compliance_test():
    passed_tests = 0

    for idx, test in enumerate(TEST_CASES):
        print(f"\n====================================================")
        print(f"🏃 Running Test {idx+1}/{len(TEST_CASES)}: {test['name']}")
        print(f"====================================================")

        # Query local vector DB for specific policy context matching the test major
        db_results = collection.query(query_texts=[f"Prerequisites for {test['major']}"], n_results=4)
        retrieved_policies = "\n".join(db_results['documents'][0])

        courses_str = "\n".join([f"- {c}: Grade {g}" for c, g in test['completed_courses'].items()])

        # Minified orchestration prompt for fast automated evaluation passes
        test_prompt = f"""
        Act as a strict compliance verification algorithm. Evaluate this student state against UMich rules.
        RULES: {rules.PREREQUISITES}
        STUDENT: Major: {test['major']}, GPA: {test['gpa']}, History: {courses_str}. Constraints: {test['constraints']}
        RAG CONTEXT: {retrieved_policies}

        Respond with a raw JSON object matching this structure exactly. Do not wrap in markdown code blocks:
        {{"passed_validation": true, "evaluation_summary": "Why they passed or failed compliance constraints"}}
        """

        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=test_prompt,
                config=types.GenerateContentConfig(response_mime_type="application/json")
            )

            output_json = json.loads(response.text)
            summary = output_json.get("evaluation_summary", "").lower()

            print(f"🤖 AI Audit Result: {output_json.get('evaluation_summary')}")

            # Assertion Check: Verify if the AI caught the expected critical condition keywords
            if test["must_contain_keyword"] in summary:
                print("✅ TEST PASSED: AI accurately mapped structural alignment rules.")
                passed_tests += 1
            else:
                print(f"❌ TEST FAILED: AI did not capture the required structural restriction rule constraint ('{test['must_contain_keyword']}').")

        except Exception as e:
            print(f"💥 TEST CRASHED: Runtime compilation issue: {e}")

    print(f"\n📊 FINAL RESULTS: Passed {passed_tests}/{len(TEST_CASES)} validation scenarios.")

if __name__ == "__main__":
    run_compliance_test()
