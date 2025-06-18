import requests
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    encoded_query = requests.utils.quote(query)
    api_url = f"https://api.1688.com/suggestion/ajax.json?keywords={encoded_query}&pageSize=20"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Referer": f"https://m.1688.com/offer_search/-{encoded_query}.html"
    }

    try:
        res = requests.get(api_url, headers=headers)
        data = res.json()
        products = []

        # Example format: Adjust depending on actual JSON keys
        for item in data.get('result', []):
            products.append({
                'title': item.get('name'),
                'link': item.get('url'),
                'image': item.get('image', '')
            })

        return jsonify({
            'query': query,
            'search_url': api_url,
            'products': products
        })

    except Exception as e:
        return jsonify({
            'error': str(e),
            'query': query,
            'products': []
        })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
