#!/usr/bin/python3
"""This module contains API routes"""

from flask import Flask, jsonify, request
import requests
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JSONIFY_MIMETYPE'] = 'application/json'


@app.route('/api/hello', methods=['GET'], strict_slashes=False)
def hello():
    """Return a welcome message"""
    name = request.args.get('visitor_name')
    if name is None:
        return jsonify({"error": "Missing query parameter"}), 400

    name = name.replace('"', '')
    message = {}
    city = ''

    if "X-Forwarded-For" in request.headers:
        client_ip = request.headers.getlist('X-Forwarded-For')[0]
    else:
        client_ip = request.remote_addr

    api_key = "f1184544951945c7abfbc4e04698c89e"
    temp_key = "1ff422a4b69845fdb26132503240307"

    api_url = f"https://api.ipgeolocation.io/ipgeo?apiKey={api_key}&ip={client_ip}"
    # api_url = "https://api.ipgeolocation.io/ipgeo"
    # api_url = f"https://ipapi.co/{client_ip}/json/"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        city = data.get("city")

        message["client_ip"] = f"{client_ip}"
        message["location"] = f"{city}"
    else:
        return jsonify({
            "error": "Failed to retrieve location data",
            "client_ip": f"{client_ip}",
            "code": response.status_code,
            "name": name
            }), 400

    temp_url = f"https://api.weatherapi.com/v1/current.json?key={temp_key}&q={city}"
    temp_response = requests.get(temp_url)

    if temp_response.status_code == 200:
        temp_data = temp_response.json()
        temp = temp_data.get("current").get("temp_c")

        message["greeting"] = f"Hello, {name}!, the temperature is {temp}degrees Celcius in {city}"
    else:
        return jsonify({"error": "Failed to retrieve temperature data"}), 400

    return jsonify(message), 200


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
