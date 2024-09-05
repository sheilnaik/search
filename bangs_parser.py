import json
import os
import re
from jsonschema import validate, ValidationError

# Load and validate the bangs JSON file against the schema
def load_bangs():
    try:
        # Load the schema
        with open("bangs.schema.json", "r") as schema_file:
            schema = json.load(schema_file)
        
        # Load the bangs data
        with open("bangs.json", "r") as bangs_file:
            bangs_data = json.load(bangs_file)
        
        # Validate the bangs data against the schema
        validate(instance=bangs_data, schema=schema)
        
        # Build a dictionary for easy lookup by trigger
        bangs_dict = {bang["t"]: bang for bang in bangs_data}
        return bangs_dict
    except ValidationError as e:
        print(f"Schema validation error: {e}")
        return {}
    except Exception as e:
        print(f"Error loading bangs: {e}")
        return {}

# Parse the query and return the corresponding search URL
def parse_bang(query, bangs_dict):
    words = query.strip().split()
    
    if not words:
        return None

    # Extract the bang trigger from the first word
    bang_trigger = words[0].lstrip('!')  # Remove leading '!' if present
    search_terms = " ".join(words[1:])

    # Check if the bang trigger exists in the bangs dictionary
    if bang_trigger in bangs_dict:
        bang = bangs_dict[bang_trigger]
        # Replace {{{s}}} with the search terms, handling URL encoding
        search_url = bang["u"].replace("{{{s}}}", re.sub(r'\s+', '+', search_terms))
        return search_url
    
    return None

# Example usage
if __name__ == "__main__":
    bangs_dict = load_bangs()
    
    # Test queries
    test_queries = [
        "!0bo Avengers",
        "!1001 climate change",
        "normal search"
    ]

    for query in test_queries:
        result = parse_bang(query, bangs_dict)
        if result:
            print(f"Redirect to: {result}")
        else:
            print(f"No bang found for: {query}")
