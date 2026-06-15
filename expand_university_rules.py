import chromadb

# Connect to your existing local database
chroma_client = chromadb.PersistentClient(path="./chroma_storage")
collection = chroma_client.get_collection(name="umich_academic_rules")

# Structured core prerequisite data for UMich Computer Science
core_curriculum_rules = [
    "EECS 280 (Programming and Data Structures) requires a grade of C or better in EECS 183 or ENGR 101.",
    "EECS 203 (Discrete Math) requires a grade of C or better in MATH 115 or equivalent calculus background.",
    "EECS 281 (Data Structures and Algorithms) strictly requires a grade of C or better in BOTH EECS 280 AND EECS 203. No concurrent enrollment allowed.",
    "EECS 370 (Introduction to Computer Organization) requires a grade of C or better in EECS 280 and concurrent or prior enrollment in EECS 203.",
    "EECS 376 (Foundations of Computer Science) requires a grade of C or better in BOTH EECS 280 AND EECS 203.",
    "UMich CS Upper-Level Electives (ULCs) generally require a grade of C or better in EECS 281. Students cannot enroll in 400-level CS electives until EECS 281 is successfully passed with a C or higher.",
    "To officially declare the Computer Science Major in the College of Engineering, a student must complete pre-declaration courses (EECS 183, EECS 280, EECS 203, MATH 115, MATH 116) with a cumulative pre-declaration GPA of 2.5 or higher and a grade of C or better in each course."
]

print("Adding UMich CSE Core Curriculum and Prerequisite rules to ChromaDB...")

# Generate simple IDs for these new text blocks
rule_ids = [f"core_rule_{i}" for i in range(len(core_curriculum_rules))]

# Inject them directly into your database
collection.add(
    documents=core_curriculum_rules,
    ids=rule_ids
)

print("🎉 Success! Your vector database now understands the entire core CS course pathway.")
