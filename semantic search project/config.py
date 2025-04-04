import os


# Get the path of  where config.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define the data directory as a folder named data
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

# Define the relative paths
RAW_CSV_FILE = os.path.join(DATA_DIR, "products_data.csv")
CLEANED_CSV_FILE = os.path.join(DATA_DIR, "cleaned_products_data.csv")
EMBEDDINGS_FILE = os.path.join(DATA_DIR, "product_embeddings.json")

# Model configuration
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
DEVICE = "cpu"

# Encoding settings
CSV_ENCODING = "utf-8"

# Batch size for encoding
BATCH_SIZE = 16

# Display progress bar during encoding
SHOW_PROGRESS_BAR = True
print("config set")
