# api.py
import os
from flask import Flask, request, jsonify
from map import compute_route  # Import the core logic

app = Flask(__name__)

@app.route('/get_route', methods=['POST'])
def get_route_api():
    # Extract JSON data from the request
    data = request.get_json()
    source = data.get("source")
    destination = data.get("destination")
    
    if not source or not destination:
        return jsonify({"error": "Missing source or destination."}), 400

    # Use the core backend logic to compute the route
    result = compute_route(source, destination)

    # Check if an error was returned and set an appropriate status code
    if "error" in result:
        return jsonify(result), 400

    return jsonify(result), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use PORT from env, default to 5000 locally
    app.run(host='0.0.0.0', port=port)

