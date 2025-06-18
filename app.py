import requests
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

RAPIDAPI_KEY = "b01bd03224mshb0e039c6191ca74p1ffe48jsne113075021df"
RAPIDAPI_HOST = "1688-datahub1.p.rapidapi.com"

@app.route('/search')
def search():
    query = request.args.get('q', 'shoes')
    
    url = "https://1688-datahub1.p.rapidapi.com/item_search"

    headers = {
        "x-rapidapi-host": RAPIDAPI_HOST,
        "x-rapidapi-key": RAPIDAPI_KEY
    }

    params = {
        "keyword": query,
        "page": 1,
        "pageSize": 10
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        # Optional: just return the products only
        products = data.get('data', {}).get('data', [])
        return jsonify({
            "query": query,
            "results": products
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Required for Render
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
