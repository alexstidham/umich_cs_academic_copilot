# 〽️ UMich CS Academic Copilot & Multi-Year RAG Planner

A production-grade, hybrid artificial intelligence application designed to architect compliant, multi-semester graduation schedules for University of Michigan Computer Science students. This system utilizes a dual-layer architecture combining a deterministic structural rules engine with semantic vector database retrieval to eliminate LLM hallucinations.

## 🚀 Key Architectural Features Implemented

* **The Deterministic Truth Layer (`curriculum_rules.py`)**: Built a hardcoded prerequisite dependency graph in Python to structurally validate course tracks (e.g., locking Upper-Level Electives until EECS 281 is passed with a C or better) before parsing contextual logic.
* **Semantic Policy Tracking (RAG Layer)**: Utilized a local persistent **ChromaDB vector database** to embed and query unstructured University Program Guide policy blocks, allowing the AI to weigh soft parameters like capstone options and dual-counting restrictions.
* **Deterministic Structured JSON Processing**: Configured the **Gemini 2.5 Flash API** using explicit schema mime-types to guarantee minified JSON outputs, enabling data to feed cleanly into native frontend visualization components.
* **Performance Session Caching (`st.cache_data`)**: Implemented deep backend state caching within the **Streamlit web framework** to mitigate redundant database vector scans and slash API execution token overhead to 0.0 seconds on identical profile re-runs.
* **Automated Compliance Test Suite (`test_suite.py`)**: Engineered a Test-Driven Development (TDD) automated validation script to stress-test high-variance edge cases (such as the notorious pre-declaration C- grade retake constraint) with explicit string validation criteria.

---

## 🛠️ Tech Stack & Dependencies

* **Language/Runtime:** Python 3.11+
* **Core GenAI Orchestration:** Google GenAI SDK (`gemini-2.5-flash`)
* **Vector Database Infrastructure:** ChromaDB (Persistent local storage)
* **Frontend Dashboard Platform:** Streamlit Web Framework
* **Local Workspace Engineering:** Python-Dotenv, Watchdog Hot-Reload Engine

---

## 🏃 Setup & Execution Instructions

### 1. Initialize Local Environment
Clone this repository to your local workspace, configure your Python virtual environment, and install the structural tracking manifests:

```bash
# Clone the repository
git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
cd YOUR_REPO_NAME

# Setup and trigger the virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install deterministic dependencies
pip install -r requirements.txt
