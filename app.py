import requests
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

RAPIDAPI_HOST = "1688-datahub1.p.rapidapi.com"
RAPIDAPI_KEY = "b01bd03224mshb0e039c6191ca74p1ffe48jsne113075021df"  # 🔒 for testing only

@app.route('/search')
def search():
    query = request.args.get('q', '')
    
    url = f"https://{RAPIDAPI_HOST}/offer_search"
    params = {
        "keywords": query,
        "page": "1"  # You can make this dynamic
    }

    headers = {
        "x-rapidapi-host": RAPIDAPI_HOST,
        "x-rapidapi-key": RAPIDAPI_KEY,
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        # Extract product info
        products = []
        for item in data.get("data", {}).get("data", []):
            products.append({
                "title": item.get("subjectTrans", ""),
                "image": item.get("imageUrl", ""),
                "price": item.get("priceInfo", {}).get("price", ""),
                "sold": item.get("monthSold", ""),
                "link": f"https://detail.1688.com/offer/{item.get('offerId')}.html"
            })

        return jsonify({
            "query": query,
            "results": products
        })

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
