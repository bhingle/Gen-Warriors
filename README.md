# AI Open-Source Dependency Guardian

## Problem Statement
Open-source projects rely on hundreds of dependencies. Outdated or vulnerable packages are a top cause of security breaches and technical debt. **According to the 2025 OSSRA (Open Source Security and Risk Analysis) report, 86% of codebases contain vulnerable open source and 90% are more than four years out-of-date**. Most small teams and individual developers lack automated tools to check and fix these issues.

## Solution
AI Open-Source Dependency Guardian automates dependency risk assessment by scanning common project files (requirements.txt, package.json) and leveraging trusted vulnerability databases.

- Detects outdated or vulnerable packages by cross-referencing the National Vulnerability Database (NVD) and Open Source Vulnerabilities (OSV).

- Calculates a Dependency Risk Score (0–100) by weighting vulnerabilities based on severity (Critical, High, Medium, Low) and the number of affected packages.

- Generates a risk report with detailed business impact and safe upgrade recommendations using Google Gemini.

- Auto-creates a patched dependency file with updated stable versions, making it simple to copy or replace in your project.

- Tracks project dependency health over time by storing previous scans and highlighting improvements or regressions using built-in memory.

## Architecture 

![Architecture Diagram](/Gen-Warriors/src/media/AI%20Open-Source%20Guardian-Arch.png)

## 🔧 Components

### 1️⃣ User Interface
- **Framework:** Streamlit  
- **Responsibilities:**
  - Handles file uploads (`requirements.txt` / `package.json`).
  - Displays:
    - 📊 Risk Score
    - 📦 Dependency Analysis
    - 📥 Patched File Download

---

### 2️⃣ Agent Core
- **Planner:**
  - Parses dependency files.
  - Generates tasks for vulnerability and risk analysis.
  - Decides whether to use cached `last_scan` or trigger a fresh scan.

- **Executor:**
  - Builds structured JSON prompt for Gemini.
  - Calls **Google Gemini API** to:
    - Get CVSS scores & severity.
    - Generate risk explanation.
    - Suggest patched versions.
  - Generates patched dependency file (`requirements.txt` or `package.json`).

- **Memory:**
  - Stores scan results in `data_db.json`.
  - Tracks:
    - Risk scores
    - Suggested fixes
    - Scan timestamps
  - Calculates improvement/regression between scans.
  - Maintains a max of 10 entries (FIFO cleanup).

---

### 3️⃣ Tools / APIs
- **Google Gemini API**
  - Core engine for vulnerability analysis & risk scoring.
- **Local Parsers**
  - `parse_dependency_file()` for Python and Node.js dependency files.

---

### 4️⃣ Observability
- **Debug Logging:**
  - Parsed dependencies
  - Combined dependency dictionary
  - Raw Gemini response
  - Suggested versions
- **Error Handling:**
  - `try/except` around Gemini API call and memory storage.
  - Fallback defaults if Gemini JSON parsing fails.
  - User-friendly error messages in the UI.
- **Retries:**
  - Resilient against malformed responses.
  - Auto-cleanup of temporary files after scan.


## Setup & Installation
1. Clone the repo and `cd` into the project directory.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Add your Gemini API key to a `.env` file:
   ```
   GEMINI_API_KEY=your-gemini-api-key-here
   ```

## Usage
1. Prepare a `requirements.txt` file (or `package.json`).
2. Run the CLI:
   ```
   streamlit run src/streamlit_ui.py
   ```
3. Enter the path to your dependency file when prompted.
4. View the risk report and find the patched file in the same directory.

## Gemini Integration
- The agent uses Gemini to analyze dependencies, explain risks, and suggest safe upgrades.
- See `src/gemini_api.py` and `src/executor.py` for integration details.

## Future Improvements
- **Interactive Chatbot Mode:** Enable follow-up questions and conversational analysis, transforming the tool into an intelligent dependency advisor.

- **File Versioning:** Maintain version history for each scanned file to track dependency changes and risk evolution over time.

- **Real-Time CVE Integration:** Connect directly to live CVE databases (NVD, OSV) via APIs for up-to-the-minute vulnerability data.

- **Automated PR Generation:** Automatically create pull requests with patched dependency files for seamless integration into CI/CD pipelines.


