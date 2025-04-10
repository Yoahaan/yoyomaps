# api.py
import os
from flask import Flask, request, jsonify
from map import compute_route  # Import the core logic
import requests

app = Flask(__name__)

@app.route('/', methods=['GET'])
def root():
    return jsonify({"message": "API is up and running"}), 200


# get_route endpoint for route fetching
@app.route('/get_route', methods=['POST'])
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

    
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
