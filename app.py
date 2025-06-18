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

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        products = []

        # Attempt to find offer items — HTML structure may need adjusting
        for item in soup.select('a'):  # You may narrow this with class names
            title = item.get_text(strip=True)
            link = item.get('href')
            if title and link and 'offer' in link:
                products.append({
                    'title': title,
                    'link': link
                })

        return jsonify({
            "query": query,
            "search_url": search_url,
            "products": products[:10]  # Limit for preview
        })

    except Exception as e:
        return jsonify({
            "error": str(e),
            "query": query,
            "search_url": search_url
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
