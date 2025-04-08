#  Semantic Search System for Product Data

## Project Overview
This project implements a **semantic search system** using `SentenceTransformers` and `Typesense`. Unlike traditional keyword-based searches, this system **understands the meaning** of user queries and retrieves the most relevant product results.

The system consists of several key components, including **web scraping, data processing, semantic embeddings, and a command-line interface (CLI)** for user interaction.

---

## 📂 Project Phases

### 1️. Data Collection (Phase 1)
- **Web Scraping:**  
  Uses `Selenium` to extract product data from websites, handling **multiple pages** and **dynamic content**.
- **Data Storage:**  
  Saves data into `data.json`, which will be processed later.

### 2️. Data Processing & Indexing (Phase 2)
- **Embedding Generation:**  
  Uses `SentenceTransformer` (`paraphrase-multilingual-MiniLM-L12-v2`) to generate **vector embeddings** from product titles and descriptions.
- **Typesense Indexing:**  
  Creates a **Typesense collection** and indexes data with a schema for **fast, efficient searches**.

### 3️. Search & CLI Interaction
- **User Query Input:**  
  Users enter queries via the **command-line interface (CLI)**.
- **Semantic Search:**  
  Queries are converted into embeddings, and the system retrieves **the most relevant products**.
- **Result Display:**  
  Outputs **titles, descriptions, and URLs** of the most relevant products.

---

##  Key Features
 **Accurate Search Results** – Uses **semantic embeddings** to understand query intent.  
 **Optimized Resource Management** – Includes caching to prevent **model overload** and improve speed.  
 **Efficient Indexing & Retrieval** – Supports **multi-search capabilities** to **minimize API calls**.  
 **Robust Data Collection** – Uses **advanced web scraping** for accurate product extraction.  
 **User-Friendly CLI** – Provides a **structured, responsive** search experience.

---

## ⚙️ Installation Guide

### 1️. Set Up Virtual Environment

### 2️. Install Dependencies
 
Before setting up the project, ensure you have the following installed:

```
pip install -r requirements.txt
```

Docker: Install Docker to run the Typesense server. Follow the installation instructions for your operating system on the Docker website.​

Set Up Virtual Environment

It’s recommended to use a virtual environment to manage project dependencies. 

Install Dependencies
With the virtual environment activated, install the required Python packages:
      
   ```
pip install -r requirements.txt
```


# Execution Order

The project is divided into multiple scripts, each responsible for a specific phase. Run the scripts in the following order:
 1. Data Preparation & Cleaning:
 • Script: src/scraping.py , dataprep.py

 • Purpose: scrape data from the web, Clean and organize raw scraped data; save the cleaned data in the data/ folder

3. Embedding Generation:
 • Script: e.g., src/embeddingmodel.py

 • Purpose: Read the cleaned data, combine title and description, and generate vector embeddings using SentenceTransformer.


 4. Typesense Client Initialization & Schema Definition:
 • Script: e.g., src/schemma.py

 • Purpose: Initialize the Typesense client and define the collection schema.


 6. Indexing Data:
 • Script: e.g., src/indximport.py

 • Purpose: Index the data (including embeddings) into the Typesense collectionand bulk import to database.

 8. Command-Line Interface (CLI):
 • Script: e.g., src/CLI.py

 • Purpose: Launch the CLI for user queries.
 • Important:** Ensure the Typesense server is running before executing this script.

# Installation

Set Up Environment Variables
Create a .env file in the project root directory and add the following lines:
   ```
API_KEY=your_typesense_api_key(check the project document)
TYPESENSE_HOST=localhost
TYPESENSE_PORT=8108
TYPESENSE_PROTOCOL=http
COLLECTION_NAME=your_collection_nam
MODEL_NAME=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```
Replace your_typesense_api_key and your_collection_name with the mentioned API key in the document.

Run Typesense Server
Use Docker to run the Typesense server:​

```
docker run -d -p 8108:8108 --name typesense \
  -e TYPESENSE_API_KEY=your_typesense_api_key \
  typesense/typesense:0.28.0
```

# Additional Information

## Project Structure:

## Project Structure

```
Jooyeshgar/
│── Semantic search project/
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
│   ├── Requirements.txt
│   ├── Semantic search Venv/  (virtual environment folder – add to .gitignore)
│   ├── typesense_data/  (persistent Typesense data folder)
│   └── docker-compose.yml  (for running Typesense and other services)
```


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

##sample results : the item "پرینتر " is entered by the user and most relevant results are shown in order of relevance : 
![image](https://github.com/user-attachments/assets/a16ad907-a3b0-4d6a-9398-09c83db78887)
![image](https://github.com/user-attachments/assets/59da2d91-72a4-4422-b78a-3ef6e6d03bfb)



