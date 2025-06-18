import requests
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    encoded_query = requests.utils.quote(query)
    url = f"https://s.1688.com/selloffer/offer_search.htm?keywords={encoded_query}&n=y&netType=1"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36",
        "Referer": "https://www.1688.com/"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        products = []

        for div in soup.select('div.sm-offerShopwindow-title'):
            title = div.get_text(strip=True)
            link = div.find_parent('a')
            href = link['href'] if link else ''

            products.append({
                "title": title,
                "link": href
            })

        return jsonify({
            "query": query,
            "search_url": url,
            "products": products
        })

    except Exception as e:
        return jsonify({"error": str(e), "products": [], "query": query})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
