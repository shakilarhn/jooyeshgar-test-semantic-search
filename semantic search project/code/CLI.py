import os
import json
import logging
import sys
from typing import Any, Dict, List, Optional
from functools import lru_cache
from sentence_transformers import SentenceTransformer
import typesense
from dotenv import load_dotenv


load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY is not set in the environment variables.")
TYPESENSE_HOST = os.getenv("TYPESENSE_HOST", "localhost")
TYPESENSE_PORT = os.getenv("TYPESENSE_PORT", "8108")
TYPESENSE_PROTOCOL = os.getenv("TYPESENSE_PROTOCOL", "http")
COLLECTION_NAME = os.getenv("TYPESENSE_COLLECTION", "products")
MODEL_NAME = os.getenv("MODEL_NAME", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")


# Cache the SentenceTransformer model so it is loaded only once per process
@lru_cache(maxsize=1)
def get_model() -> SentenceTransformer:
    try:
        model_instance = SentenceTransformer(MODEL_NAME)
        logging.info("SentenceTransformer model loaded successfully.")
        return model_instance
    except Exception as e:
        logging.error("Error loading model. Please check configuration.")
        raise e


# Initialize the Typesense client
try:
    client = typesense.Client({
        'nodes': [{
            'host': TYPESENSE_HOST,
            'port': TYPESENSE_PORT,
            'protocol': TYPESENSE_PROTOCOL
        }],
        'api_key': API_KEY,
        'connection_timeout_seconds': 5
    })
    logging.info("Typesense client initialized successfully.")
except Exception as e:
    logging.error("Error initializing Typesense client. Please check configuration.")
    sys.exit(1)


def perform_search(query_text: str, k: int = 10) -> Optional[Dict[str, Any]]:
    """
    Convert a search query into an embedding vector, build the vector query,
    and perform a multi_search in the Typesense collection.
    """
    try:
        # Validate the query
        if not query_text.strip():
            logging.warning("Empty search query provided.")
            return None

        # Get the cached model
        model = get_model()

        # Convert the query into an embedding vector using the model
        query_embedding = model.encode(query_text).tolist()
        # Convert the embedding vector into a string to match the required format for Typesense
        vector_values = ",".join(map(str, query_embedding))
        vector_query_str = f"embedding:([{vector_values}], k:{k})"
        logging.debug(f"Vector query: {vector_query_str}")

        # Build search parameters for multi_search
        search_parameters = {
            "collection": COLLECTION_NAME,  # The collection in Typesense where we are performing the search
            "q": "*",  # Search across all documents
            "query_by": "combined_text",  # Field to search (combined text of title and description)
            "vector_query": vector_query_str  # The vector query string for the embedding
        }

        # Multi-search request body (for efficiency and future scalability)
        multi_search_body = {
            "searches": [search_parameters]  # We wrap the search parameters in the searches array
        }

        # If the 'results' key exists in the response, return the first search result.
        # Otherwise, return None indicating that no results were found.
        results = client.multi_search.perform(multi_search_body)
        return results['results'][0] if results.get('results') else None

    except Exception as error:
        logging.error("Error during search operation.")
        # Log detailed error info at DEBUG level to avoid exposing sensitive details
        logging.debug(f"Detailed error: {error}", exc_info=True)
        return None


def filter_results(matching_results: List[Dict[str, Any]]) -> None:
    """
    Sort search results by vector_distance and display formatted information

    """
    # Sort results by vector_distance for relevance order
    sorted_results = sorted(
        matching_results,
        key=lambda result: result.get('vector_distance', float('inf'))
    )
    #Format Display results
    print("\nSearch Results:")
    for result in sorted_results:
        doc = result.get('document', {})
        # Only show fields useful for the user
        filtered_doc = {key: value for key, value in doc.items() if key in ['Title', 'Description', 'URL']}
        print(json.dumps(filtered_doc, ensure_ascii=False, indent=4))
        print("-" * 40)


def main() -> None:
    print("Welcome to Jooyeshgar!")
    while True:
        query = input("What are you looking for? (type 'exit' to quit): ").strip()
        # handling user input; prompt again if input is empty
        if not query:
            print("Please enter a non-empty search query.")
            continue

        if query.lower() == "exit":
            print("Exiting the search system. Goodbye!")
            break

        results = perform_search(query)
        if results and 'hits' in results and len(results['hits']) > 0:
            filter_results(results['hits'])
        else:
            print("No results found or an error occurred.")


if __name__ == "__main__":
    main()
