import logging
from CLI import perform_search, filter_results  # Ensure 'CLI' is the correct module name

# Disable all logging messages
logging.disable(logging.CRITICAL)

def interactive_test():
    print("Welcome to the interactive search test!")
    while True:
        query = input("Please enter your search query (or type 'exit' to quit): ").strip()
        if query.lower() == "exit":
            print("Exiting the interactive test. Goodbye!")
            break
        if not query:
            print("Empty query. Please try again.")
            continue

        results = perform_search(query)
        if results and 'hits' in results and len(results['hits']) > 0:
            print("\nRetrieved Results:")
            filter_results(results['hits'])
        else:
            print("No results retrieved for your query. Please check your input or try another query.")

if __name__ == "__main__":
    interactive_test()
