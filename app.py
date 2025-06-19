import requests
from flask import Flask, request, Response
import os

app = Flask(__name__)

@app.route('/proxy')
def proxy():
    query = request.args.get('q', '')
    if not query:
        return {"error": "Missing search query"}, 400

    search_url = f"https://m.1688.com/offer_search/-{requests.utils.quote(query)}.html"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Mobile Safari/537.36',
        'Referer': 'https://m.1688.com'
    }

    try:
        r = requests.get(search_url, headers=headers, timeout=10)
        return Response(r.content, content_type=r.headers['Content-Type'])
    except Exception as e:
        return {"error": "Failed to fetch content", "details": str(e)}, 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
