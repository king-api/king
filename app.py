import requests
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup

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
