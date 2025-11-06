# python_basics examples

This folder contains small Python learning examples and tests for a 60-day AI learning project.


Quick start

1. Create a virtual environment and install test requirement:

   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

2. Run tests:

   PYTHONPATH=./src pytest -q

3. Run examples:

   PYTHONPATH=./src python examples/hello.py
   # Or run csv example, optionally pass output dir
   PYTHONPATH=./src python examples/csv_example.py /tmp

Notes
- The package root is `src/` so you must set `PYTHONPATH=./src` when running tests or examples from the project root.
- This is intentionally small and dependency-free to be easy to read and extend.
