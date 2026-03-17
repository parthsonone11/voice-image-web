from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

ACCESS_KEY = os.environ.get("UNSPLASH_KEY")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    try:
        query = request.json.get("query")

        if not query:
            return jsonify([])

        url = "https://api.unsplash.com/search/photos"

        headers = {
            "Authorization": f"Client-ID {ACCESS_KEY}"
        }

        params = {
            "query": query,
            "per_page": 6
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            return jsonify([])

        data = response.json()

        images = [img["urls"]["small"] for img in data.get("results", [])]

        return jsonify(images)

    except Exception as e:
        print("Error:", e)
        return jsonify([])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)