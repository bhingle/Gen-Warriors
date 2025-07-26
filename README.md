# AI Open-Source Dependency Guardian

## Problem Statement
Open-source projects rely on hundreds of dependencies. Outdated or vulnerable packages are a top cause of security breaches and technical debt. Most small teams and individual developers lack automated tools to check and fix these issues.

## Solution
AI Open-Source Dependency Guardian scans a project’s dependency file (requirements.txt, package.json) and:
- Detects outdated or vulnerable packages
- Assigns a Dependency Risk Score (0–100)
- Uses Gemini to generate a plain-language risk report + safe upgrade recommendations
- Auto-generates a patched dependency file with updated versions
- Tracks project dependency health over time via memory

## Architecture Diagram
```
User (CLI/Streamlit)
   ↓
Planner (planner.py)
   ↓
Executor (executor.py) ← Gemini API (gemini_api.py)
   ↓
Memory (memory.py)
   ↓
Output: Risk Report + Updated File
```

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
   python src/UI.py
   ```
3. Enter the path to your dependency file when prompted.
4. View the risk report and find the patched file in the same directory.

## Gemini Integration
- The agent uses Gemini to analyze dependencies, explain risks, and suggest safe upgrades.
- See `src/gemini_api.py` and `src/executor.py` for integration details.

## Future Improvements
- Add Streamlit web UI
- Support for `package.json` (npm projects)
- Real-time CVE database integration
- Automated PRs for dependency upgrades


