# AURA

## Autonomous Unified Reasoning & Automation Agent

**Plan. Act. Verify. Recover.**

AURA turns a natural-language goal into an observable, tool-backed workflow. It plans the work, executes registered capabilities, verifies structured outputs, recovers from bounded failures, and keeps a persistent execution trail that can be inspected from the UI or API.

```text
User goal
   -> Plan
   -> Registered tools
   -> Execute
   -> Verify
   -> Recover when needed
   -> Persist and explain
```

## What AURA Does

### Goal execution

- Rule-based planning for deterministic offline operation.
- Optional OpenAI-assisted planning when configured.
- Typed plan validation before execution.
- Registered tools only: unknown or unsafe tool names are rejected.
- Dependency-aware task ordering.
- Structured execution events, verification, retries, and failure states.

### Available capabilities

- Web search with live or explicitly configured fallback behavior.
- Web scraping through requests or Playwright modes.
- Content summarization.
- Email sending or clearly labelled simulation when SMTP is unavailable.
- Resume parsing for PDF, DOCX, and TXT files.
- Resume analysis with AI or deterministic local fallback.
- Job matching from an analyzed resume.
- Execution logging.

### User interface

The Streamlit application provides:

- A goal-first Start view.
- Resume analysis and job matching.
- Backend-backed execution History.
- Registered Capabilities with risk and retry metadata.
- Insights calculated from persisted runs.
- Live task events, verification, and recovery details.

The interface uses a warm paper canvas, navy navigation styling, coral actions, teal execution accents, modular typography, responsive spacing, and no emoji-based UI controls.

## Architecture

```text
Streamlit UI
    |
    v
FastAPI backend
    |
    +--> Planner (rule or LLM)
    |
    +--> Typed plan validation
    |
    +--> Tool registry
    |       +--> Search
    |       +--> Scraper
    |       +--> Summarizer
    |       +--> Resume tools
    |       +--> Job matcher
    |       +--> Email
    |
    +--> Task graph and controller
    |
    +--> Verification and bounded recovery
    |
    +--> Atomic JSON run store
```

The backend owns execution and persistence. The Streamlit UI calls the backend for task execution, run history, resume analysis, job matching, capabilities, and evaluation data.

## Project Structure

```text
src/
├── agent/
│   ├── controller.py       # Dependency-aware execution and events
│   ├── evaluator.py        # Metrics from persisted runs
│   ├── models.py           # Typed plans, tasks, events, and results
│   ├── planner.py          # Deterministic planner
│   ├── planner_llm.py      # Optional OpenAI planner
│   ├── recovery.py         # Failure classification and retry policy
│   ├── run_store.py        # Atomic JSON execution history
│   ├── task_graph.py       # Dependency ordering and cycle checks
│   ├── tool_registry.py    # Registered tool metadata
│   └── verifier.py         # Deterministic output verification
├── tools/                  # Independent tool adapters
├── ui/
│   ├── components.py       # Reusable Streamlit components
│   └── theme.py            # AURA visual system
├── app_gui.py              # Streamlit entry point
└── main.py                 # FastAPI entry point
tests/                     # Planner, controller, API, recovery, and verifier tests

```

## Quick Start

### Requirements

- Python 3.10 or newer.
- Optional API credentials for live OpenAI, SerpAPI, Google Search, or SMTP features.
- Optional Playwright browser installation for JavaScript-heavy pages.
- Optional Tesseract and Poppler installations for scanned PDF OCR.

### Install

```bash
git clone <repository-url>
cd Agentic-AI-automator
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add only the credentials required for the services you plan to use. `.env` is ignored by Git.

### Start the backend

```bash
uvicorn src.main:app --reload --port 8000
```

FastAPI documentation is available at [http://localhost:8000/docs](http://localhost:8000/docs).

### Start the UI

In a second terminal:

```bash
export AURA_API_URL=http://127.0.0.1:8000
streamlit run src/app_gui.py
```

Open [http://localhost:8501](http://localhost:8501).

On Windows PowerShell:

```powershell
$env:AURA_API_URL = "http://127.0.0.1:8000"
streamlit run src/app_gui.py
```

## Configuration

| Variable | Purpose | Required |
| --- | --- | --- |
| `AURA_API_URL` | Backend URL used by the UI | No, defaults to `http://127.0.0.1:8000` |
| `PLANNER_MODE` | `rule` or `llm` planner selection | No, defaults to `rule` |
| `OPENAI_API_KEY` | LLM planning and analysis | Optional |
| `SERPAPI_KEY` | Live web search | Optional |
| `GOOGLE_API_KEY` | Google Custom Search | Optional |
| `GOOGLE_CSE_ID` | Google Custom Search engine | Optional |
| `SCRAPER_MODE` | `basic` or `playwright` scraping | Optional |
| `SMTP_HOST` | SMTP server for email delivery | Optional |
| `SMTP_PORT` | SMTP server port | Optional |
| `SMTP_USER` | SMTP username | Optional |
| `SMTP_PASSWORD` | SMTP password or app password | Optional |
| `DEFAULT_FROM` | Default sender address | Optional |
| `AURA_RUN_STORE` | Custom path for persisted run records | Optional |

When a live service is not configured, AURA reports fallback, simulation, or unavailable status rather than silently claiming live external data.

## API

### Health and discovery

```text
GET /health
GET /tools
GET /metrics
GET /evaluation
```

### Run a goal

```http
POST /run
Content-Type: application/json
```

```json
{
  "goal": "Find remote Python internships and summarize the best matches",
  "planner": "rule"
}
```

The response includes a `run_id`, final status, validated plan, logs, structured events, task counts, and verification counts.

### Inspect runs

```text
GET /runs
GET /runs/{run_id}
```

### Resume workflows

```text
POST /resume/analyze
POST /resume/match
```

Resume analysis accepts a base64-encoded PDF, DOCX, or TXT payload with a 10 MB limit. The UI uses these endpoints directly, so parsing and matching remain backend-owned operations.

## Testing

Run the complete suite:

```bash
pytest -q
```

The tests cover typed plan validation, dependency ordering, verification, bounded recovery, API validation, run persistence, resume workflows, and evaluation metrics. Tests are deterministic and do not require live API credentials.

## Persistence and Privacy

Execution records are stored in `.aura_runs.json` by default. The file is ignored by Git because it can contain goals, outputs, and execution metadata. Set `AURA_RUN_STORE` to use another local path.

Do not commit `.env` files, API keys, uploaded resumes, personal documents, `.aura_runs.json`, generated reports, or sensitive logs.

External integrations may operate in fallback or simulation mode. Verify the service status before treating a result as live external data.

## Current Limitations

- The default run store is a local JSON file rather than a multi-user database.
- Some search and analysis fallbacks are intentionally lightweight.
- OCR requires system packages that are not installed by Python dependencies alone.
- LLM planner comparison requires an OpenAI configuration and real benchmark runs.
- Streamlit is designed for a local or small-team demonstration rather than high-concurrency production serving.

## Roadmap

- Benchmark suite for rule and LLM planners.
- Richer task graph visualization.
- Persistent user preference memory with secret filtering.
- More task-specific verification evidence.
- Production database and authentication boundary.

