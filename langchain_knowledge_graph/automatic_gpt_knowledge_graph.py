from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from dotenv import load_dotenv
# Load environment variables
load_dotenv()
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

# Define schema for extraction
schema = {
    "properties": {
        "person": {"type": "string"},
        "company": {"type": "string"},
        "role": {"type": "string"},
        "location": {"type": "string"},
        "relationship": {"type": "string"}
    },
    "required": ["person", "relationship"]
}


# Text to extract from
text = """
Sarah Johnson is the Chief Technology Officer at DataFlow Inc.
The company is headquartered in Mumbai, India.
Sarah previously worked with Rahul Sharma at CloudSystems.
DataFlow Inc specializes in artificial intelligence solutions.
"""



schema_list = {
    "title": "ExtractionSchema",
    "description": "Schema for extracting entities from text",
    "type": "object",
    "properties": {
        "entities": {
            "type": "array",
            "items": schema
        }
    },
    "required": ["entities"]
}

structured_llm = llm.with_structured_output(schema_list)
result = structured_llm.invoke(text)

print("Extracted entities:")
if result and "entities" in result:
    for item in result["entities"]:
        print(item)
else:
    print(result)