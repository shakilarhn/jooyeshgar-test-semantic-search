import sys
import os
import json
import logging
from typing import List, Dict, Any
import typesense
from dotenv import load_dotenv


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def load_environment_variables() -> str:

    load_dotenv()
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API_KEY is not set in the environment variables.")
    return api_key


def load_config() -> str:

    config_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if config_dir not in sys.path:
        sys.path.append(config_dir)
    try:
        from config import EMBEDDINGS_FILE
    except ImportError as e:
        raise ImportError("Could not import EMBEDDINGS_FILE from config.py") from e
    return EMBEDDINGS_FILE


def load_product_embeddings(embeddings_file: str) -> List[Dict[str, Any]]:

    try:
        with open(embeddings_file, "r", encoding="utf-8") as file:
            product_records = json.load(file)
    except FileNotFoundError as e:
        logging.error(f"Embeddings file not found: {embeddings_file}")
        raise e
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON from the embeddings file: {embeddings_file}")
        raise e
    return product_records


def update_product_ids(product_records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Ensure each product record has a unique 'id' if not assign ids to products for typesense collection

    """
    for idx, product in enumerate(product_records):
        if "id" not in product:
            product["id"] = str(idx)
    return product_records


def save_updated_embeddings(product_records: List[Dict[str, Any]], original_file: str) -> str:
    """
    Save updated product records with unique IDs to a new JSON file.

    """
    directory = os.path.dirname(original_file)
    updated_file_path = os.path.join(directory, "product_embeddings_with_id.json")
    try:
        with open(updated_file_path, "w", encoding="utf-8") as output_file:
            json.dump(product_records, output_file, ensure_ascii=False, indent=4)
    except IOError as e:
        logging.error(f"Error writing updated embeddings file: {updated_file_path}")
        raise e
    return updated_file_path


def initialize_typesense_client(api_key: str) -> typesense.Client:
    """
    Initialize and return a Typesense client using the provided API key.

    """
    client = typesense.Client({
        'nodes': [{
            'host': 'localhost',  # Your Typesense server's host
            'port': '8108',  # Default Typesense port
            'protocol': 'http'  # Use 'https' if applicable
        }],
        'api_key': api_key,
        'connection_timeout_seconds': 5
    })
    return client


def bulk_import_documents(client: typesense.Client, product_records: List[Dict[str, Any]],
                          collection_name: str = 'products') -> None:
    """
    Bulk import product records into the specified Typesense collection.

    """
    try:
        import_results = client.collections[collection_name].documents.import_(product_records, {'action': 'upsert'})
        for result in import_results:
            if not result.get('success', False):
                logging.error(f"Failed to import document: {result}")
        logging.info("Bulk import completed.")
    except Exception as e:
        logging.error(f"Error during bulk import: {e}")
        raise e


def get_collection_details(client: typesense.Client, collection_name: str = 'products') -> int:
    """
    Retrieve and return the number of documents in the specified Typesense collection.
to make sure the dataset has been successfully imported
    """
    try:
        collection = client.collections[collection_name].retrieve()
        num_documents = collection.get('num_documents', 0)
        logging.info(f"Number of documents in '{collection_name}' collection: {num_documents}")
        return num_documents
    except Exception as e:
        logging.error(f"Error retrieving collection details for {collection_name}: {e}")
        raise e


def main():

    setup_logging()
    logging.info("Starting product embeddings import process.")
    try:
        api_key = load_environment_variables()
        embeddings_file = load_config()
        product_records = load_product_embeddings(embeddings_file)
        product_records = update_product_ids(product_records)
        updated_file_path = save_updated_embeddings(product_records, embeddings_file)
        logging.info(f"Updated embeddings file saved at: {updated_file_path}")

        client = initialize_typesense_client(api_key)
        bulk_import_documents(client, product_records)
        get_collection_details(client)
    except Exception as e:
        logging.error(f"Process terminated due to an error: {e}")


if __name__ == '__main__':
    main()
