Semantic Search System for Product Data

Project Overview:

This project aims to develop a semantic search system using SentenceTransformers and Typesense.
This system allows users to input their queries(searching for a product) and receive matching results that are semantically relevant. Instead of relying solely on keyword matching, the system compares the underlying meaning of the query with the embedded representations of the product data, enabling more accurate  search capabilities.

The project is structured into several phases, each focusing on a critical component of the system, from data collection to processing and finally to search and user interaction.

Project Phases

1. Data Collection (Phase 1)
 • Web Scraping:
web scraping techniques are employed ,using Selenium ,to extract product data from the website. This phase involves navigating through multiple pages, handling dynamic content, and robustly capturing key product details such as titles, descriptions, and URLs.

 • Data Storage:
The collected data is initially stored in a structured JSON file (data.json). This file serves as the raw data source, which is later cleaned, processed, and indexed for semantic search.

3. Data Processing and Indexing (Phase 2)
 • Embedding Generation:
In this phase, we use the SentenceTransformer model (specifically, paraphrase-multilingual-MiniLM-L12-v2) to convert textual data into high-dimensional vector embeddings. By combining both the title and description of each product, the model creates a comprehensive semantic representation for each item. This enables the system to understand and match the meaning behind user queries.
 • Typesense Indexing:
Once the embeddings are generated, we create a new collection within Typesense. The collection is configured with a well-defined schema that includes fields for product title, description, URL, and the corresponding embedding vector. Indexing the data in Typesense allows us to perform fast and efficient vector searches, making it possible to retrieve the most relevant products based on semantic similarity.

4. Search Functionality and CLI Interface
 • User Query Input:
A command-line interface (CLI) has been developed to interact with the system. Users can type in  queries directly into the terminal.
 • Semantic Search:
When a query is entered, it is first converted into an embedding using the same SentenceTransformer model. The system then performs a vector search within the Typesense collection, to rank the results by semantic closeness to return the most relevant results.
 • Result Display:
The search results are presented to the user in a clear and organized format, showing key details (such as the product title, description, and URL) of the most relevant found items.

Key Features
 • Enhanced Search Accuracy and resource management:
By using semantic embeddings, the system retrieves products that are contextually relevant to user queries rather than just matching keywords. By adding caching options we avoid the model from overloading and we improve pace and manage the resource.
 • Robust Data Collection:
Advanced web scraping techniques ensure that product data is accurately and reliably captured from dynamic websites.
 • Efficient Indexing and Retrieval:
with multi-search capabilities we reduce the number of API calls and improve overall search speed.
 • User-Friendly CLI:
The command-line interface offers a simple and effective way for users to perform searches and view results, making the system accessible even without a graphical user interface. the command line is well-structured for times when the input query isn't valid. 



Before setting up the project, ensure you have the following installed:

Docker: Install Docker to run the Typesense server. Follow the installation instructions for your operating system on the Docker website.​

Set Up Virtual Environment

It’s recommended to use a virtual environment to manage project dependencies. 

Install Dependencies
With the virtual environment activated, install the required Python packages:
pip install -r requirements.txt

Execution Order

The project is divided into multiple scripts, each responsible for a specific phase. Run the scripts in the following order:
 1. Data Preparation & Cleaning:
 • Script: src/scraping.py , dataprep.py
 • Purpose: scrape data from the web, Clean and organize raw scraped data; save the cleaned data in the data/ folder

2. Embedding Generation:
 • Script: e.g., src/embeddingmodel.py
 • Purpose: Read the cleaned data, combine title and description, and generate vector embeddings using SentenceTransformer.


 3. Typesense Client Initialization & Schema Definition:
 • Script: e.g., src/schemma.py
 • Purpose: Initialize the Typesense client and define the collection schema.


 4. Indexing Data:
 • Script: e.g., src/indximport.py
 • Purpose: Index the data (including embeddings) into the Typesense collectionand bulk import to database.

 6. Command-Line Interface (CLI):
 • Script: e.g., src/CLI.py
 • Purpose: Launch the CLI for user queries.
 • Important:** Ensure the Typesense server is running before executing this script.

Installation
Set Up Environment Variables
Create a .env file in the project root directory and add the following lines:
API_KEY=your_typesense_api_key(check the project document)
TYPESENSE_HOST=localhost
TYPESENSE_PORT=8108
TYPESENSE_PROTOCOL=http
COLLECTION_NAME=your_collection_nam
MODEL_NAME=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2

Replace your_typesense_api_key and your_collection_name with the mentioned API key in the document.

Run Typesense Server
Use Docker to run the Typesense server:​

docker run -d -p 8108:8108 --name typesense \
  -e TYPESENSE_API_KEY=your_typesense_api_key \
  typesense/typesense:0.28.0

Additional Information

Project Structure:
Jooyeshgar/
├── Semantic search project/
│   ├── Code/
│   │   ├── Scraping.py
│   │   ├── Dataprep.py
│   │   ├── Embeddingmodel.py
│   │   ├── Schema.py
│   │   ├── Indximport.py
│   │   ├── CLI.py
│   │   └── .env
│   ├── Data/
│   │   ├── Products_data.csv
│   │   ├── Cleaned_products_data.csv
│   │   ├── Product_embedding.json
│   │   └── Product_embeddings_with_id.json
│   ├── Config.py
│   └── Requirements.txt
├── Semantic search Venv/   (virtual environment folder – add to .gitignore)
├── typesense_data/         (persistent Typesense data folder)
└── docker-compose.yml      (for running Typesense and other services)

Explanation
 • Jooyeshgar/
The root directory of your overall project.

 • Semantic search project/
Contains all the project files:

 • Code/: Contains Python scripts:
 
    • Scraping.py: Web scraping logic.
    • Dataprep.py: Data cleaning and preparation functions.
    • Embeddingmodel.py: Script for generating embeddings using SentenceTransformer.
    • Schema.py: Defines the Typesense schema.
    • Indximport.py: Script to index data into Typesense.
    • CLI.py: Command-line interface for search queries.
    • .env: Environment variables configuration file.
   
 • Data/:Contains data files:
 
    • Products_data.csv: Raw scraped product data.
    • Cleaned_products_data.csv: Data after cleaning.
    • Product_embedding.json: Embeddings file.
    • Product_embeddings_with_id.json: Embeddings with IDs for indexing.
    • Config.py: A script for global project configuration.
    • Requirements.txt: List of Python dependencies.
   
 • Semantic search Venv/
The virtual environment for your project. This folder should be excluded from GitHub using .gitignore.

 • typesense_data/
Folder used for persistent storage by the Typesense server when running in Docker.

 • docker-compose.yml
Docker Compose file to run Typesense (and other services, if needed) in a containerized environment.
  


