from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    url = "https://1688-datahub1.p.rapidapi.com/item_search"

    headers = {
        "x-rapidapi-host": "1688-datahub1.p.rapidapi.com",
        "x-rapidapi-key": "b01bd03224mshb0e039c6191ca74p1ffe48jsne113075021df"
    }

    params = {
        "keyword": query,
        "page": 1,
        "pageSize": 10
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        items = data.get("data", {}).get("data", [])

        # Extract simplified info
        results = []
        for item in items:
            results.append({
                "title": item.get("subjectTrans"),
                "image": item.get("imageUrl"),
                "price": item.get("priceInfo", {}).get("price"),
                "sold": item.get("monthSold"),
                "offerId": item.get("offerId")
            })

        return jsonify({
            "query": query,
            "results": results
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
