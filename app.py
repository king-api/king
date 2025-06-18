import requests
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    if not query:
        return jsonify({"error": "Query param 'q' is required"}), 400

    encoded_query = requests.utils.quote(query)
    search_url = f"https://m.1688.com/offer_search/-{encoded_query}.html"

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10)"
    }

    try:
        res = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')

        results = []

        # Parse item list (simplified — will refine based on 1688 structure)
        for item in soup.select('.item'):  # This selector may need tuning
            title = item.select_one('.title').get_text(strip=True) if item.select_one('.title') else 'No Title'
            image = item.select_one('img')['src'] if item.select_one('img') else ''
            price = item.select_one('.price').get_text(strip=True) if item.select_one('.price') else 'N/A'
            link = item.get('href', '#')

            results.append({
                "title": title,
                "image": image,
                "price": price,
                "link": link
            })

        return jsonify({
            "query": query,
            "results": results
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
