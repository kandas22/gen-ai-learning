# GenAI Learning

This repository contains small, focused example projects for learning Python, browser automation using Playwright, and web application development using Streamlit. It is organized into subdirectories; each subdirectory includes its own README with detailed usage notes and examples:

- `python_basics/` — small Python examples, exercises and tests.
- `playwright_basics/` — Playwright-based browser automation examples and tests.
- `streamlit_webapp/` — Interactive web applications built with Streamlit.

Quick overview
--------------

Each top-level folder is self-descriptive and contains a `README.md` that explains how to use the code inside that folder. Before running examples or tests, create and activate a virtual environment in the repository root and install dependencies.

Create and activate a virtual environment (macOS / Linux):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Notes:
- If a subfolder ships its own `requirements.txt`, install that as well (for example, `playwright_basics` may require Playwright and pytest-asyncio).
- The Python package root for examples in this repo is `src/`. Many examples and tests assume `PYTHONPATH=./src` when run from the project root.

python_basics
-------------

The `python_basics/` directory contains small, dependency-light Python examples and tests intended for learning core language features and small utilities.

Common commands (from repo root):

```bash
# Run tests in python_basics (ensure PYTHONPATH points to src)
PYTHONPATH=./src pytest python_basics -q

# Run a simple example
PYTHONPATH=./src python python_basics/examples/hello.py
```

See `python_basics/README.md` for more examples, file-by-file descriptions, and extra notes.

streamlit_webapp
--------------

The `streamlit_webapp/` directory contains interactive web applications built using Streamlit. It includes two example applications:

1. Hello World App (`src/myapp.py`) - A simple greeting application demonstrating basic Streamlit features:
   - Text input for user name
   - Dynamic greeting updates
   - Basic styling and layout

2. Calculator App (`src/calculator.py`) - An interactive calculator with:
   - Numeric input fields
   - Operation selection (Addition, Subtraction, Multiplication, Division)
   - Real-time calculation
   - Error handling (e.g., division by zero)
   - Styled UI elements

Common commands (from streamlit_webapp directory):

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Hello World app
streamlit run src/myapp.py

# Run the Calculator app
streamlit run src/calculator.py

# Run all tests
pytest tests/
```

See `streamlit_webapp/README.md` for detailed setup instructions, testing guidelines, and troubleshooting tips.

playwright_basics
-----------------

The `playwright_basics/` directory demonstrates browser automation using Playwright (async API). It contains utility modules, tests, and example runner scripts such as `examples/browser_example.py` and `examples/form_example.py`.

Before running Playwright examples follow these extra steps after activating the virtual environment:

```bash
# Install Playwright Python (if not already installed via requirements.txt)
pip install playwright

# Download browser binaries used by Playwright (Chromium, Firefox, WebKit)
playwright install
```

Run an example (from repo root):

```bash
.venv/bin/python playwright_basics/examples/browser_example.py
# or (example that interacts with a form)
.venv/bin/python playwright_basics/examples/form_example.py
```

Tests in `playwright_basics` use the async Playwright API and pytest-asyncio. See `playwright_basics/README.md` for notes about test instability, Playwright versions, headless flags, and troubleshooting steps.

Refer to subfolder READMEs
-----------------------

Each subdirectory (`python_basics/`, `playwright_basics/`) contains a `README.md` with specific usage instructions, examples, and any extra setup steps required by that module. If you're working on a particular area, open that folder's README first.

Troubleshooting
---------------

- If you see import errors, make sure `PYTHONPATH=./src` is set or install the package in editable mode:

```bash
pip install -e .
```

- Playwright browser crashes or timeouts: try running in headed mode (remove `headless=True`), increase timeouts, or upgrade/downgrade the Playwright package to a version compatible with your platform.

- If tests fail with event-loop or pytest-asyncio errors, ensure `pytest-asyncio` is installed and that tests use async APIs consistently. See `playwright_basics/README.md` for a recommended pytest configuration.

Contributing / Next steps
-------------------------

- Add new examples under the appropriate folder and document them in that folder's README.
- If you change dependencies, update `requirements.txt` and mention any Playwright browser installation steps in `playwright_basics/README.md`.

Questions or problems?
---------------------

Open an issue or contact the repository maintainer for help. If you'd like, I can also update any sub-README with more examples or create CI for running the Playwright examples on a schedule.

Repo Maintainer : kandas22@gmail.com
