# `text_splitter.py` usage

## Requirements
- Python 3.11 (matches `.venv`)
- The project virtual environment at `/Users/kanda/Learning/GenAI/gen-ai-learning/.venv`
- Packages installed inside that venv:
  - `langchain`
  - `langchain-community`
  - `langchain-text-splitters`
  - `pypdf` (for `PyPDFLoader`)
  - `tiktoken`
  - `torch` (only if `transformers` pulls it in for your loaders)

Install them with:

```
cd /Users/kanda/Learning/GenAI/gen-ai-learning
source .venv/bin/activate
python -m pip install langchain langchain-community langchain-text-splitters pypdf tiktoken torch
```

> If your shell aliases `python` to the system interpreter, run `unalias python`
> after activating the venv, or call the interpreter explicitly via
> `./.venv/bin/python`.

## Place the PDF to split
`text_splitter.py` expects `LLM.pdf` in the same directory (`langchain_learning/`).

## Run the script

```
cd /Users/kanda/Learning/GenAI/gen-ai-learning/langchain_learning
../.venv/bin/python text_splitter.py
```

This loads `LLM.pdf`, concatenates the page text, splits it into 200-character
chunks (no overlap), and prints the resulting list to stdout.

## Adjustments
- Change `chunk_size`/`chunk_overlap` in `text_splitter = RecursiveCharacterTextSplitter(...)`
  to suit your downstream model.
- Replace `LLM.pdf` with any other PDF by editing the `PyPDFLoader` path.


