from flask import Flask, request, redirect, jsonify
import os

# Import the bangs parser functions
from bangs_parser import load_bangs, parse_bang

app = Flask(__name__)

# Load the bangs dictionary when the app starts
bangs_dict = load_bangs()

# Route to handle search queries
@app.route('/search')
def search():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    # Parse the query to find a bang and construct the search URL
    search_url = parse_bang(query, bangs_dict)
    
    if search_url:
        return redirect(search_url)
    else:
        # Fallback to Google search if no bang is found
        google_search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        return redirect(google_search_url)

# Health check endpoint
@app.route('/health')
def health():
    return jsonify({"status": "OK"})

if __name__ == '__main__':
    app.run(debug=True)
