# curriculum_rules.py

# Strict prerequisite matrix for the entire UMich CS Curriculum
PREREQUISITES = {
    # Pre-Declaration & Core Prerequisites
    "EECS 183": [],
    "ENGR 101": [],
    "MATH 115": [],
    "MATH 116": ["MATH 115"],
    "EECS 280": ["EECS 183"],  # Can also be ENGR 101
    "EECS 203": ["MATH 115"],

    # Core Major Requirements
    "EECS 281": ["EECS 280", "EECS 203"],
    "EECS 370": ["EECS 280"],   # Co-req or pre-req: EECS 203
    "EECS 376": ["EECS 280", "EECS 203"],

    # Major Upper-Level Electives (ULCs) & Common Electives
    "EECS 482": ["EECS 281", "EECS 370"],         # Operating Systems
    "EECS 485": ["EECS 281"],                      # Web Systems
    "EECS 445": ["EECS 281", "MATH 214"],          # Machine Learning (Requires Linear Algebra)
    "EECS 492": ["EECS 281"],                      # Artificial Intelligence
    "EECS 484": ["EECS 281"],                      # Database Management Systems
    "EECS 442": ["EECS 281", "MATH 214"],          # Computer Vision
    "EECS 493": ["EECS 281"],                      # User Interface Design

    # Foundational Math Electives
    "MATH 214": ["MATH 116"],                      # Applied Linear Algebra
    "MATH 215": ["MATH 116"],                      # Calculus III
    "STATS 250": ["MATH 115"],                     # Intro to Stats and Data Analysis
    "STATS 412": ["MATH 116"]                      # Intro to Probability
}

# Categorized tracking buckets to ensure graduation compliance
DEGREE_REQUIREMENTS = {
    "PRE_DECLARATION": ["EECS 183", "EECS 280", "EECS 203", "MATH 115", "MATH 116"],
    "CORE": ["EECS 281", "EECS 370", "EECS 376"],
    "ELECTIVES_REQUIRED_COUNT": 4, # Typically requires 4 Upper-Level CS Electives (16 credits)
    "MATH_ELECTIVE_OPTIONS": ["MATH 214", "MATH 215", "MATH 216", "MATH 425"],
    "STATS_ELECTIVE_OPTIONS": ["STATS 250", "STATS 412", "STATS 426"]
}

def verify_schedule_logic(completed_courses, target_course):
    """
    Deterministically checks if a student has legally cleared a course's prerequisites
    based on the strict structural rules.
    """
    if target_course not in PREREQUISITES:
        return True, "Course not tracked in core graph, passing to AI fallback analysis."

    required = PREREQUISITES[target_course]
    missing = []

    for req in required:
        # Check if they completed it AND if they earned a valid passing grade (C or better)
        if req not in completed_courses:
            missing.append(req)
        elif completed_courses[req] in ["C-", "D+", "D", "D-", "E", "F"]:
            missing.append(f"{req} (Retake Required - current grade is {completed_courses[req]})")

    if missing:
        return False, f"⚠️ Cannot schedule {target_course}. Missing prerequisites: {', '.join(missing)}"
    return True, "Cleared"
