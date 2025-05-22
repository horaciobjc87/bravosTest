from flask import Flask, jsonify 
from urllib import request
import json

app = Flask(__name__)
API_BASE_URL = "https://dogapi.dog/api/v2"

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
    return response

def fetch_data(endpoint):
    try:
        with request.urlopen(f"{API_BASE_URL}{endpoint}") as response:
            data = response.read().decode()
            return json.loads(data)
    except Exception as e:
        print(f"Error fetching {endpoint}: {e}")
        return {"Error": str(e)}
    
@app.route("/breeds", methods = ["GET"])
def get_breeds():
    return jsonify(fetch_data("/breeds"))

@app.route("/breeds/<breed_id>", methods = ["GET"])
def get_breeds_id(breed_id):
    data = fetch_data(f"/breeds/{breed_id}")
    return jsonify(data)

@app.route("/facts", methods = ["GET"])
def get_facts():
    return jsonify(fetch_data("/facts"))

@app.route("/groups", methods = ["GET"])
def get_groups():
    return jsonify(fetch_data("/groups"))

@app.route("/groups/<group_id>", methods = ["GET"])
def get_groups_id(group_id):
    data = fetch_data(f"/groups/{group_id}")
    return jsonify(data)

@app.route("/group-details/<group_id>", methods=["GET"])
def get_group_details(group_id):
    group = fetch_data(f"/groups/{group_id}")
    breeds = fetch_data("/breeds")
    
    if "data" in group and "data" in breeds:
        related_breeds = [
            breed for breed in breeds["data"]
            if breed["relationships"]["group"]["data"] and
               breed["relationships"]["group"]["data"]["id"] == group_id
        ]
        return jsonify({
            "group": group["data"],
            "breeds": related_breeds
        })
    return jsonify({"error": "Unable to fetch group details"}), 500

@app.route("/group-details/<group_id>/breed/<breed_id>", methods = ["GET"])
def get_groups_details_id_breed_id(group_id, breed_id):
    group = fetch_data(f"/groups/{group_id}")
    breeds = fetch_data(f"/breeds/{breed_id}")
    
    if "data" in group and "data" in breeds:
        related_breeds_group = (
            breeds["data"]["relationships"]["group"]["data"] and
            breeds["data"]["relationships"]["group"]["data"]["id"] == group_id
        )
        return jsonify({
            "group": group["data"],
            "breed": breeds["data"],
            "relation": related_breeds_group,
        })
    return jsonify({"error": "Unable to fetch group details"}), 500

if __name__ == "__main__":
    app.run(debug=True)

#@app.route("/group-details", methods = ["GET"])
#def get_groups_details():
#    return jsonify(fetch_data("/groups-details"))