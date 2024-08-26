# Laptop Data Scraper and Analyzer

This project provides a set of simple tools for scraping text data related to laptops, extracting structured information using a Large Language Model (LLM), and performing basic analysis on the extracted data.

## Features

  **Web Scraping**: Gather data from a German Electronics online shop.
  
  **Data Extraction**: Use a LLM to convert unstructured text into structured data (e.g., brand, price, CPU, ...).
  
  **Data Analysis**: Perform simple analyses on the extracted data.

## Setup

The project is equipped with a Dockerfile and a development container for easy setup and deployment.

### Fetching the LLM

To fetch the Large Language Model used for data extraction, run the following command:

`huggingface-cli download bartowski/gemma-2-9b-it-GGUF --include "gemma-2-9b-it-Q6_K_L.gguf" --local-dir ./models`

*Note: You can fetch any LLM that suits your GPU capabilities. The model above works well for this project and requires about 8 GB of VRAM.*
*Also, please note that this setup has been tested with a 40xx NVIDIA GPU. Other configurations have not been tested.*
