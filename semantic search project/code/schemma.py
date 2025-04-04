import os
import logging
import typesense
from dotenv import load_dotenv

# Setup logging configuration for better output control
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

load_dotenv()

api_key = os.getenv('API_KEY')
if not api_key:
    raise ValueError("API_KEY is not set in the environment variables.")

# Initialize the Typesense client using the API key from the environment
client = typesense.Client({
    'nodes': [{
        'host': 'localhost',   # Your Docker container is accessible here
        'port': '8108',        # Default Typesense port
        'protocol': 'http'
    }],
    'api_key': api_key,
    'connection_timeout_seconds': 5
})

logging.info("Typesense client initialized successfully.")

# Define the collection schema
schema = {
    "name": "products",
    "fields": [
        {"name": "id", "type": "string"},
        {"name": "Title", "type": "string"},
        {"name": "Description", "type": "string"},
        {"name": "URL", "type": "string"},
        {"name": "combined_text", "type": "string"},
        {"name": "embedding", "type": "float[]", "num_dim": 384}
    ]
}

# Attempt to create the collection; if it already exists, log the error
try:
    client.collections.create(schema)
    logging.info("Collection 'products' created successfully.")
except Exception as e:
    logging.error(f"Collection creation failed or collection already exists: {e}")
