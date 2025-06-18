import requests
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    encoded_query = requests.utils.quote(query)
    search_url = f"https://s.1688.com/selloffer/offer_search.htm?keywords={encoded_query}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122 Safari/537.36"
    }

    try:
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        products = []
        for item in soup.select('.offer-list-row .offer-title'):
            title = item.get_text(strip=True)
            link = item.get('href')
            if title and link:
                products.append({'title': title, 'link': link})

        return jsonify({
            'query': query,
            'search_url': search_url,
            'products': products
        })

    except Exception as e:
        return jsonify({
            'error': str(e),
            'query': query,
            'search_url': search_url,
            'products': []
        })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
