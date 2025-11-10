# GPT-2 Text Generation

This project demonstrates text generation using the Hugging Face Transformers library with the GPT-2 model.

## Description

`ai_gp2.py` uses the GPT-2 model to generate text based on a given prompt. It creates a text generation pipeline and generates creative continuations of the input text.

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. Install the required dependencies:

```bash
pip install transformers torch
```

Or if you have a `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## Usage

Run the script directly:

```bash
python ai_gp2.py
```

The script will generate text based on the prompt "Once upon a time" and print the result.

### Customize the Prompt

To use a different prompt, modify the `prompt` variable in the script:

```python
prompt = "Your custom prompt here"
```

### Adjust Generation Parameters

You can modify the generation parameters:

- `max_length`: Maximum length of generated text (default: 30)
- `num_return_sequences`: Number of different sequences to generate (default: 1)

Example:

```python
print(generator(prompt, max_length=50, num_return_sequences=3))
```

## How It Works

1. The script imports the `pipeline` function from the transformers library
2. Creates a text generation pipeline using the GPT-2 model
3. Generates text based on the provided prompt
4. Returns the generated text

## Expected Output

The script will output generated text that continues from the prompt "Once upon a time". Example:

```
Once upon a time, there was a young girl who lived in a small village...
```

## Notes

- First run may take longer as it downloads the GPT-2 model (~500MB)
- Subsequent runs will use the cached model
- Generated text may vary between runs due to the model's probabilistic nature

## Troubleshooting

If you encounter issues:

1. Ensure you have a stable internet connection for the first run (model download)
2. Check that you have sufficient disk space (~500MB for the model)
3. Verify your Python version: `python --version`

