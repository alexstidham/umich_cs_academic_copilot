import json

print("=== 〽️ UMich Academic Advisor Onboarding ===")
print("Let's capture your status, grades, and academic constraints.\n")

major = input("What is your major (e.g., Computer Science)? ")
current_term = input("What is your next upcoming semester (e.g., Fall 2026)? ")

while True:
    try:
        gpa = float(input("What is your cumulative GPA (e.g., 3.42)? "))
        if 0.0 <= gpa <= 4.0: break
        print("❌ GPA must be between 0.0 and 4.0.")
    except ValueError:
        print("❌ Please enter a valid decimal number.")

# New Structured Course + Grade Capture Loop
completed_courses = {}
print("\n--- Course History Entry ---")
print("Enter your completed courses one by one with their final letter grade.")
print("Type 'done' when you are finished adding classes.\n")

while True:
    course = input("Course name (e.g., EECS 183) or 'done': ").strip().upper()
    if course == 'DONE':
        break
    if not course:
        continue

    grade = input(f"What letter grade did you get in {course} (e.g., B+, C-)? ").strip().upper()
    completed_courses[course] = grade

print("\n--- Edge Cases & Constraints ---")
constraints = input("Describe any special scenarios (e.g., 'Want a light load', 'Need term off'): ")

# Package the structured data
profile_data = {
    "major": major.strip(),
    "current_term": current_term.strip(),
    "gpa": gpa,
    "completed_courses": completed_courses, # This is now a dictionary!
    "constraints": constraints.strip()
}

with open("student_profile.json", "w") as f:
    json.dump(profile_data, f, indent=4)

print("\n Success! Structured profile saved to 'student_profile.json'.")
