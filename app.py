import streamlit as st
import os
import json
import chromadb
from dotenv import load_dotenv
from google import genai
from google.genai import types # Import types for structured schema execution
import curriculum_rules as rules

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

st.set_page_config(page_title="UMich CS Academic Advisor Pro", page_icon="〽️", layout="wide")

st.title("〽️ UMich Computer Science Academic Copilot (Enterprise Pro)")
st.caption("Hybrid Architecture: Combining a Deterministic Structural Dependency Graph with Contextual RAG Embedding Lookups.")

# Sidebar Setup
st.sidebar.header("🎓 Student Profile Setup")
major = st.sidebar.selectbox("Select Major", ["Computer Science", "Data Science"])
current_term = st.sidebar.selectbox("Target Entry Semester", ["Fall 2026", "Winter 2027", "Fall 2027"])
gpa = st.sidebar.slider("Cumulative GPA", 0.0, 4.0, 3.2, step=0.01)

st.sidebar.markdown("---")
st.sidebar.subheader("📚 Course History Tracker")

completed_courses = {}
all_tracked_courses = sorted(list(rules.PREREQUISITES.keys()))

for course in all_tracked_courses:
    taken = st.sidebar.checkbox(f"Attempted {course}")
    if taken:
        grade = st.sidebar.selectbox(f"Grade for {course}", ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "E"], key=f"grade_{course}")
        completed_courses[course] = grade

st.sidebar.markdown("---")
constraints = st.sidebar.text_area("Constraints / Custom Edge Cases", placeholder="e.g., 'Want to focus on Web Systems path', 'Need a light load'")

# --- DEFINE STREAMLIT CACHING FUNCTION ---
# This prevents redundant API charges if inputs haven't changed!
@st.cache_data(show_spinner=False)
def call_advisor_engine(major, current_term, gpa, completed_courses, constraints, retrieved_policies):
    courses_str = "\n".join([f"- {c}: Grade {g}" for c, g in completed_courses.items()])

    master_prompt = f"""
    You are a senior Academic Advisor for the UMich CS program. Review this profile and output a strict JSON array of semesters.

    STRICT COMPLIANCE:
    - Any core class with a C- or below MUST be retaken immediately next semester.

    STUDENT INPUT:
    - Major: {major}, Start: {current_term}, GPA: {gpa}
    - History: {courses_str}
    - Constraints: {constraints}

    RULES FROM DB:
    {retrieved_policies}

    You MUST respond with a JSON object matching this schema exactly. Do not wrap it in markdown block tags, return raw JSON text:
    {{
        "assessment": "Brief string summary of student standing",
        "warnings": ["Warning 1", "Warning 2"],
        "schedule": [
            {{"semester": "Fall 2026", "courses": ["EECS 280", "MATH 214"], "reasoning": "Retaking 280 due to prior C- grade."}},
            {{"semester": "Winter 2027", "courses": ["EECS 281", "EECS 370"], "reasoning": "Unlocked by completing 280."}}
        ]
    }}
    """

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=master_prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json" # <--- Force structured JSON output
        )
    )
    return json.loads(response.text)

# --- UI SPLIT LAYOUT ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📋 Rule-Engine Validation Check")
    structural_warnings = []
    for course, grade in completed_courses.items():
        if grade in ["C-", "D+", "D", "D-", "E", "F"] and course in rules.DEGREE_REQUIREMENTS["PRE_DECLARATION"] + rules.DEGREE_REQUIREMENTS["CORE"]:
            structural_warnings.append(f"❌ **{course}** grade was **{grade}**. Departmental rules require an immediate retake.")

    if structural_warnings:
        for warning in structural_warnings: st.error(warning)
    else:
        st.success("✅ No prerequisite grade violations identified.")

    st.markdown("---")
    st.write("Dynamic RAG Retrieval Inspect Layer:")
    # RAG Configuration Sliders (Milestone 2 Sneak Peek!)
    rag_k = st.slider("ChromaDB Document Chunk Fetch (k)", 1, 10, 4)

with col2:
    st.subheader("🤖 Generated Academic Roadmap")

    if st.button("Generate Strategic Multi-Year Schedule", type="primary"):
        with st.spinner("Processing local dependency paths and querying RAG context vectors..."):

            # 1. Advanced RAG Retrieval Pipeline Execution
            try:
                chroma_client = chromadb.PersistentClient(path="./chroma_storage")
                collection = chroma_client.get_collection(name="umich_academic_rules")

                # Dynamic Search Query Generation based on user state
                rag_query = f"Prerequisites grading policies graduation track requirements for {major}"

                db_results = collection.query(
                    query_texts=[rag_query],
                    n_results=rag_k
                )
                retrieved_policies = "\n".join(db_results['documents'][0])

            except Exception as e:
                st.error(f"ChromaDB Link Interrupted: {e}")
                retrieved_policies = "Standard CS rule set active."
                db_results = None

            # 2. Run our cached structured JSON pipeline
            result_json = call_advisor_engine(major, current_term, gpa, completed_courses, constraints, retrieved_policies)

            # --- NEW FEATURE: VISUAL RAG INSPECTION LAYER FOR INTERVIEWERS ---
            with st.expander("🛠️ DEVELOPER CONSOLE: Inspect RAG Vector Retrieval Layer", expanded=False):
                st.markdown("#### Vector Database Pipeline Metrics")
                st.write(f"**Target Semantic Query:** `{rag_query}`")
                st.write(f"**Chunks Requested ($k$):** {rag_k}")

                if db_results and 'documents' in db_results:
                    st.markdown("---")
                    st.markdown("#### Retrieved Database Sub-Chunks (Ranked by Distance)")

                    # Loop through the retrieved documents to display their raw structural metrics
                    for idx, doc in enumerate(db_results['documents'][0]):
                        # ChromaDB returns distance scores if computed
                        score = db_results['distances'][0][idx] if 'distances' in db_results and db_results['distances'] else "N/A"
                        chunk_id = db_results['ids'][0][idx]

                        st.markdown(f"**📄 Chunk Reference:** `{chunk_id}` | **Similarity Distance Score:** `{score}`")
                        st.code(doc, language="text")
                else:
                    st.warning("No live vectors returned from local persistent disk storage.")

            st.markdown("---")

            # 3. Display Assessment Cleanly
            st.markdown(f"### 📊 Advisor Assessment")
            st.info(result_json.get("assessment", "Profile processed successfully."))

            # 4. Render Beautiful Native Streamlit Data Tables!
            st.markdown("### 🗓️ Multi-Semester Timeline Schedule")

            for index, term in enumerate(result_json.get("schedule", [])):
                with st.expander(f"➔ {term['semester']}", expanded=True):
                    cols = st.columns(len(term['courses']) if term['courses'] else 1)
                    for i, course in enumerate(term['courses']):
                        cols[i].button(course, key=f"btn_{index}_{i}", disabled=True)
                    st.caption(f"**Rationale:** {term['reasoning']}")

            # 5. Render Warnings Block
            if result_json.get("warnings"):
                st.markdown("### ⚠️ Critical Advising Warnings")
                for warning in result_json["warnings"]:
                    st.warning(warning)

