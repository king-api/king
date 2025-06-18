import requests
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

RAPIDAPI_KEY = "b01bd03224mshb0e039c6191ca74p1ffe48jsne113075021df"

@app.route('/search')
def search():
    query = request.args.get('q', '')
    url = "https://1688-datahub1.p.rapidapi.com/api/1688/product/search"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "1688-datahub1.p.rapidapi.com"
    }
    params = {
        "keyword": query,
        "page": "1",
        "sortType": "default"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        products = []

        for item in data.get('data', {}).get('data', []):
            products.append({
                "title": item.get("subjectTrans"),
                "image": item.get("imageUrl"),
                "price": item.get("priceInfo", {}).get("price"),
                "sold": item.get("monthSold"),
            })

        return jsonify({
            "query": query,
            "results": products
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
