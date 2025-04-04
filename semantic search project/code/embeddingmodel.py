import os
import sys
import json
import logging
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

def setup_logging() -> None:

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
# Load the cleaned CSV data into a DataFrame
def load_cleaned_data(csv_file: str, encoding: str) -> pd.DataFrame:

#check if loading is successful
    try:
        df = pd.read_csv(csv_file, encoding=encoding)
        logging.info(f"Loaded data from {csv_file}.")
    except Exception as e:
        logging.error(f"Failed to load CSV file {csv_file}: {e}")
        raise
    return df


def generate_embeddings(
        df: pd.DataFrame,
        model_name: str,
        device: str,
        batch_size: int,
        show_progress_bar: bool
) -> np.ndarray:

    """
    Generate embeddings for combined text from the DataFrame using SentenceTransformer.
 it combines the 'Title' and 'Description' fields into 'combined_text' for the embedding model.
    """

    if "Title" not in df.columns or "Description" not in df.columns:
        raise ValueError("DataFrame must contain 'Title' and 'Description' columns.")

    # Combine the Title and Description fields for embedding generation
    df["combined_text"] = df["Title"] + ". " + df["Description"]
    logging.info("Combined 'Title' and 'Description' into 'combined_text'.")

    # Load the SentenceTransformer model using details from config.
    model = SentenceTransformer(model_name, device=device)
    logging.info("Generating embeddings...")

    # Encode the combined text.
    embeddings = model.encode(
        df["combined_text"].tolist(),
        batch_size=batch_size,
        show_progress_bar=show_progress_bar
    )
    return np.array(embeddings)

#Save the DataFrame (with embeddings) to a JSON file.
def save_embeddings_to_json(df: pd.DataFrame, output_file: str, encoding: str) -> None:

    if "embedding" not in df.columns:
        logging.warning("DataFrame does not contain an 'embedding' column.")
    data = df.to_dict(orient="records")
    try:
        with open(output_file, "w", encoding=encoding) as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logging.info(f"Embeddings saved to {output_file}.")
    except Exception as e:
        logging.error(f"Failed to write JSON file {output_file}: {e}")
        raise

"""
making sure the model has done a great job by checking how similar some products are or  based on their semantic embeddings
how similar they are to themselves before importing to typesens 
"""

#To compute the cosine similarity between the embedding vectors of two products by part of their title
def compute_similarity(embeddings: np.ndarray, df: pd.DataFrame, title1: str, title2: str) -> None:
    try:
        # Find the index of the first product whose title contains the substring title1
        idx1 = df[df["Title"].str.contains(title1)].index[0]

        # Find the index of the first product whose title contains the substring title2
        idx2 = df[df["Title"].str.contains(title2)].index[0]

        # Compute cosine similarity between the embeddings of the two selected products
        similarity = cosine_similarity([embeddings[idx1]], [embeddings[idx2]])[0][0]

        # Log the matched product titles
        logging.info(f"Product 1 Title: {df.iloc[idx1]['Title']}")
        logging.info(f"Product 2 Title: {df.iloc[idx2]['Title']}")

        # Log the similarity score (how semantically similar the two products are)
        logging.info(f"Cosine similarity: {similarity:.3f}")

    except IndexError:
        # If no match is found for one or both product titles, log an error
        logging.error("One or both products not found in the dataset.")

#function to print the top N similar products based on the similarity matrix
def print_top_similar_products(similarity_matrix, df, product_idx, top_n=5):

    #Print the top N similar products based on the cosine similarity matrix.
    similar_indices = similarity_matrix[product_idx].argsort()[-top_n-1:-1][::-1]  # Get indices of top N similar products
    for idx in similar_indices:
        logging.info(f"Similar Product: {df.iloc[idx]['Title']} with Similarity: {similarity_matrix[product_idx][idx]:.3f}")


# Main function to execute the embedding generation, similarity computation, and save the results
def main():
    """
    Main function to generate embeddings, save them to a JSON file, and compute example similarities.
    """

    # Set up logging configuration
    setup_logging()

    #Add the parent directory to the system path
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if parent_dir not in sys.path:
        sys.path.append(parent_dir)

    #Import the configuration module (config.py) to access model settings
    try:
        import config
    except ImportError as e:
        logging.error("Could not import config module.")
        raise e

    #Load the cleaned product data from CSV
    df = load_cleaned_data(config.CLEANED_CSV_FILE, config.CSV_ENCODING)

    #Generate embeddings for the combined 'Title' and 'Description' columns
    embeddings = generate_embeddings(
        df,
        model_name=config.MODEL_NAME,
        device=config.DEVICE,
        batch_size=config.BATCH_SIZE,
        show_progress_bar=config.SHOW_PROGRESS_BAR
    )

    #Compute the cosine similarity matrix (optional for future sorting or recommendations)
    similarity_matrix = cosine_similarity(embeddings)
    logging.info("Cosine similarity matrix computed.")

    #Add the embeddings to the DataFrame
    df["embedding"] = [emb.tolist() for emb in embeddings]

    #Save the embeddings to a JSON file for further use
    save_embeddings_to_json(df, config.EMBEDDINGS_FILE, config.CSV_ENCODING)

    #Example - Compute similarity between two specific products using their titles
    compute_similarity(embeddings, df, "پرینتر سه بعدی رزینی", "پرینترهای چاپ کارت")

    #Log the dimensionality of the embedding vectors (length of embedding vectors)
    if len(embeddings) > 0:
        logging.info(f"Embedding dimensionality: {len(embeddings[0])}")
    else:
        logging.warning("No embeddings were generated.")

if __name__ == '__main__':
    main()