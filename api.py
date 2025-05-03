# api.py
import os
from flask import Flask, request, jsonify
from map import compute_route  # Import the core logic
import requests
import time

app = Flask(__name__)

@app.route('/', methods=['GET'])
def root():
    return jsonify({"message": "API is up and running"}), 200


# get_route endpoint for route fetching
@app.route('/get_route', methods=['POST'])   #this endpoint is for getting the route
def get_route_api():
    data = request.get_json()
    source = data.get("source")
    destination = data.get("destination")

    if not source or not destination:
        return jsonify({"error": "Missing source or destination."}), 400

    result = compute_route(source, destination, k=3)

    if "error" in result:
        return jsonify(result), 400

    return jsonify(result), 200

@app.route('/auto_complete', methods=['GET'])
def auto_complete():
    start = time.time()
    
    
    query = request.args.get("q")
    pune_bbox = "73.7,18.4,74.0,18.7"
    if not query:
        return jsonify({"error": "Missing query parameter"}), 400

    try:
        response = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": query, "format": "json", "limit": 5, "bounded": 1,
                "viewbox": pune_bbox }, # Restricting the search to Pune},
            headers={"User-Agent": "yoyo-maps-app"}
        )
        data = response.json()
        suggestions = [
            {
                "display_name": item["display_name"],
                "lat": item["lat"],
                "lon": item["lon"]
                
            }
            for item in data
        ]
        return jsonify(suggestions), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch suggestions"}), 500
    
@app.route('/ping')
def ping():
    return 'pong - 200 OK', 200



    
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


    
