import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/search')
def search():
    q = request.args.get('q', '')
    if not q:
        return jsonify({"error": "No query"}), 400

    url = "https://1688-datahub1.p.rapidapi.com/api/search"
    headers = {
        "X-RapidAPI-Key": os.environ.get("RAPIDAPI_KEY"),
        "X-RapidAPI-Host": "1688-datahub1.p.rapidapi.com"
    }
    params = {"keyword": q, "page": 1}

    try:
        resp = requests.get(url, headers=headers, params=params, timeout=10)
        data = resp.json()

        products = data.get("products", [])

        return jsonify({"query": q, "results": products})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
