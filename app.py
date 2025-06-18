import requests
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    encoded_query = requests.utils.quote(query)
    search_url = f"https://m.1688.com/offer_search/-{encoded_query}.html"

    return jsonify({
        "query": query,
        "search_url": search_url
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
