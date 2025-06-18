import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    if not query:
        return jsonify({"error": "Query param 'q' is required"}), 400

    api_url = f"https://m.1688.com/offer_search/ajax.html?keywords={requests.utils.quote(query)}"

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10)"
        }
        res = requests.get(api_url, headers=headers, timeout=10)
        data = res.json()

        results = []
        for item in data.get("data", []):
            results.append({
                "title": item.get("title", ""),
                "price": item.get("price", ""),
                "image": item.get("imageUrl", ""),
                "link": item.get("detailUrl", "")
            })

        return jsonify({
            "query": query,
            "results": results
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
  if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

