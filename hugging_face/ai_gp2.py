# Output: Generated text based on the prompt "Once upon a time"
# This code uses the Hugging Face Transformers library to create a text generation pipeline using the GPT-2 model.
# and defines a function to generate text based on a given prompt.
from transformers import pipeline
generator = pipeline('text-generation', model='gpt2')
# Example usage
if __name__ == "__main__":
    prompt = "Once upon a time"
    print(generator(prompt, max_length=30, num_return_sequences=1)[0]['generated_text'])
