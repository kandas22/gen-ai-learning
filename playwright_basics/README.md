Playwright Basics — Running the browser_example.py

This README explains how to set up the project, create / activate the virtual environment, install Playwright and browsers, and run the example script at `examples/browser_example.py`.

The Goal
---------
Create a Python script that regularly visits a list of specified URLs, performs a series of checks, and reports the results.

Key Automation Steps
- Read Target URLs: Load a list of URLs and expected content/performance thresholds from a configuration file (e.g., CSV ).
- Visit each URL using Playwright in (headless) browser mode.
- Measure performance (page load time) and capture HTTP status codes via network interception.
- Assert presence of critical elements using selectors and record pass/fail.
- Capture screenshots or page HTML for failures for later analysis.
- Aggregate results and append to a CSV or send to a monitoring endpoint.

Why This Is a Great Idea
-------------------------
Practicality: It solves a real-world problem in DevOps and Quality Assurance.

Feature Coverage: It uses essential Playwright features: headless browsing, network interception (to check status codes), performance measurement, element selection and assertion, and screenshot capturing.

Extensibility: You can easily extend this to include login flows, multi-step transaction monitoring, or integration with a CI/CD pipeline (using GitHub Actions/GitLab CI).

Prerequisites
- macOS (tested)
- Python 3.11+ installed
- Git (optional)

Quick start — step-by-step

1) Open a terminal and change into the project folder

```bash
cd /Users/kanda/Learning/GenAI/gen-ai-learning/playwright_basics
```

2) Create (if needed) and activate the virtual environment

```bash
# Create a venv named .venv (run only if .venv does not exist)
python -m venv .venv

# Activate it (macOS / Linux - zsh / bash)
source .venv/bin/activate
```

Note: this project may already contain a `.venv` folder. If so, just activate it.

3) Install Python dependencies

```bash
pip install -r requirements.txt
```

4) Install Playwright browsers

```bash
# This downloads Chromium, Firefox and WebKit used by Playwright
playwright install
```

5) Run the example script

```bash
# Use the virtualenv's Python to run the example
.venv/bin/python examples/browser_example.py
```

Notes & useful options

- Run in non-headless mode for debugging: by default Playwright launches browsers headless. To debug visually, edit `examples/browser_example.py` and change the browser launch to:

```py
browser = await playwright.chromium.launch(headless=False)
```

Then re-run the script from step 5.

- If VS Code shows "Import 'playwright.async_api' could not be resolved":
  - Ensure you selected the `.venv` Python interpreter in VS Code (Cmd+Shift+P -> "Python: Select Interpreter" -> choose `./.venv/bin/python`).
  - Reload the window (Cmd+Shift+P -> "Developer: Reload Window").

- If you see Playwright browser crashes (SIGSEGV) when running tests or examples:
  - Try `playwright install --with-deps` to install system dependencies (Linux only).
  - Run a single example first (not the entire test suite) to narrow down the issue.
  - Try launching Chromium non-headless to observe the crash.

Running tests

This project contains pytest tests under `tests/`. Run them with the virtualenv Python:

```bash
# Run the entire suite (may be slower / flaky depending on local environment)
.venv/bin/python -m pytest -q

# Run a single focused test (faster when debugging)
.venv/bin/python -m pytest tests/test_form_utils.py::test_fill_form -q
```

Where to find outputs

- The example script prints status information to stdout. If you enable diagnostic capture (screenshot / HTML) those files will be written next to the project root with filenames such as `debug_<host>_YYYYMMDD_HHMMSS.png` and `.html`.

Troubleshooting checklist

- Make sure the virtualenv is activated when installing and running.
- Confirm Playwright browsers are installed (`playwright install`).
- If tests fail due to async event loop errors, check `pytest-asyncio` version compatibility and confirm no other tools are running an event loop in the same process.

If you'd like, I can:
- Add a small CLI flag to the example to toggle headless vs. non-headless behavior without editing the file.
- Add a short `Makefile` with common commands (`install`, `run-example`, `test`).

Want me to add either of those enhancements?