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
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36 Chrome/122.0.0.0 Mobile Safari/537.36"
    }

    try:
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        products = []
        for item in soup.select('a.offer'):
            title = item.get('title') or item.text.strip()
            link = item.get('href')
            img = item.select_one('img')
            image_url = img['data-lazyload-src'] if img and 'data-lazyload-src' in img.attrs else (img['src'] if img else '')

            if title and link:
                products.append({
                    'title': title,
                    'link': link,
                    'image': image_url
                })

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
