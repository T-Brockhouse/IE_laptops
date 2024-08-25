# fetch model, depending on VRAM
# huggingface-cli download bartowski/gemma-2-9b-it-GGUF --include "gemma-2-9b-it-Q6_K_L.gguf" --local-dir ./models

# Imports
from datetime import datetime, timedelta
from langchain_community.llms import LlamaCpp
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.prompts import PromptTemplate

import pandas as pd
import json
import time

# Start the timer
start_time = time.time()

df=pd.read_csv("data/scraped_laptops.csv")

# run all LLM layers on GPU, adjust if needed
n_gpu_layers=-1

# Make sure the model path is correct for your system!
llm = LlamaCpp(
    model_path="models/gemma-2-9b-it-Q6_K_L.gguf",
    n_gpu_layers=n_gpu_layers,
    temperature=0.0,
    verbose=False
)

# Create prompt template
template = """You are tasked with the extraction of information about a specific laptop. If information is unavailable, do not make anything up and just leave the field empty.

### Laptop information:
{laptop_description}
    
Please format your answer in JSON with the following key/value pairs:
[
    {{
        "brand": "Name of the brand",
        "model name": "Name of the model",
        "CPU": "Name of the CPU",
        "RAM": "Amount of RAM as an integer",
        "disk space": "Amount of disk space",
        "GPU": "Name of the GPU"
    }}
]

Your answer should only consist of the JSON without any additional text or explanations.
"""

prompt=PromptTemplate.from_template(template)


def invoke_llm(laptop_str):
    """
    Function to invoke llm
    """
    llm_chain= prompt | llm

    answer=llm_chain.invoke({"laptop_description":laptop_str})

    print(answer)  

    return answer

# Function to parse JSON and create columns
def parse_json_to_columns(json_str):
    """
    Function to parse json to columns and delete "```JSON .... ```" which is always included in the answers by Gemma 9B.
    """
    # Remove triple backticks if they exist
    if json_str.startswith("```") and json_str.endswith("```"):
        json_str = json_str[7:-3].strip()
    
    # Check if the json_str is empty or None after stripping
    if not json_str or json_str == "":
        return pd.Series()

    try:
        data = json.loads(json_str)[0]  # Parse the JSON string
        return pd.Series(data)
    except json.JSONDecodeError:
        print(f"Invalid JSON: {json_str}")
        return pd.Series()  # Return an empty series if JSON is invalid

# Apply on entire df
df[['answer']] = df.apply(lambda row: pd.Series(invoke_llm(row['Title'])), axis=1)

# Apply parsing function to each row
df = df.join(df['answer'].apply(parse_json_to_columns))

# Rename columns
df.rename(columns={'model name': 'model_name', 'disk space': 'disk_space'}, inplace=True)

# Save the df
df.to_csv("data/scraped_laptops_with_specs.csv", index=False)

# End the timer
end_time = time.time()

# Calculate and print the elapsed time
elapsed_time = end_time - start_time

print(f"Script executed in {elapsed_time:.2f} seconds.")