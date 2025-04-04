import sys
import os
# Insert the parent directory  into sys.path so that config.py can be imported.
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
import config
from bs4 import BeautifulSoup
from cleantext import clean
import pandas as pd


# Remove HTML tags using BeautifulSoup.
def clean_html(text):
    if not isinstance(text, str):
        return text
    return BeautifulSoup(text, "html.parser").get_text()


# Clean and standardize the text using the clean-text library.
def clean_text(text):
    if not isinstance(text, str):
        return text
    return clean(text,
                 fix_unicode=True,  # Fix any broken or non-standard Unicode characters.
                 to_ascii=False,  # Preserve native characters.
                 lower=False,  # Retain original casing.
                 no_line_breaks=True,  # Remove line breaks.
                 no_urls=True,  # Remove URLs.
                 no_emails=True,  # Remove email addresses.
                 no_phone_numbers=True,  # Remove phone numbers.
                 no_numbers=False,  # Keep numbers.
                 no_digits=False,  # Keep digits.
                 no_currency_symbols=False,  # Keep currency symbols.
                 no_punct=False,  # Keep punctuation.
                 replace_with_url="<URL>",  # Placeholder for removed URLs.
                 replace_with_email="<EMAIL>",  # Placeholder for removed emails.
                 replace_with_phone_number="<PHONE>",  # Placeholder for removed phone numbers.
                 replace_with_number="<NUMBER>",  # Placeholder for removed numbers.
                 replace_with_digit="0",  # Placeholder for removed digits.
                 replace_with_currency_symbol="<CUR>",  # Placeholder for removed currency symbols.
                 lang="fa"  # Specify language.
                 )


# Preprocess the dataset by cleaning and standardizing the 'Title' and 'Description' columns.
def preprocess_data(input_file, output_file):
    # Load the dataset from the raw CSV file.
    df = pd.read_csv(input_file, encoding=config.CSV_ENCODING)

    # Clean HTML tags from the 'Title' and 'Description' columns.
    df['Title'] = df['Title'].apply(clean_html)
    df['Description'] = df['Description'].apply(clean_html)

    # Replace missing values with a placeholder.
    df.fillna("Information Not Available", inplace=True)

    # Remove duplicate rows.
    df.drop_duplicates(inplace=True)

    # Apply text cleaning to the 'Title' and 'Description' columns.
    df['Title'] = df['Title'].apply(clean_text)
    df['Description'] = df['Description'].apply(clean_text)

    # Save the cleaned DataFrame to the cleaned CSV file.
    df.to_csv(output_file, index=False, encoding=config.CSV_ENCODING)
    return df


# Run the preprocessing pipeline.
def run_preprocessing_pipeline():
    """
    Preprocess the product data by cleaning HTML tags and standardizing text,
    then save the cleaned data to a CSV file. then check the results by
    printing details from the first product in the cleaned dataset.
    """
    # Get file paths from config.py.
    input_csv = config.RAW_CSV_FILE
    output_csv = config.CLEANED_CSV_FILE

    # Preprocess data and save output.
    df_cleaned = preprocess_data(input_csv, output_csv)

    # Reload the cleaned data for verification.
    df_reloaded = pd.read_csv(output_csv, encoding=config.CSV_ENCODING)

    # Print details of the first product if data exists.
    if not df_reloaded.empty:
        product = df_reloaded.iloc[0]
        print(f"Title: {product['Title']}")
        print(f"Description: {product['Description']}")
        print(f"URL: {product['URL']}")
    else:
        print("The cleaned data is empty.")


if __name__ == "__main__":
    run_preprocessing_pipeline()
