import json
from src.api.maesk import maesk_get_location, maesk_get_ship_price
from src.webdriver import get_token
from user_secrets import akamai_telemetry
from flask import Flask, jsonify, request
from flask_cors import CORS
from time import sleep
from werkzeug.exceptions import HTTPException
from scrapper_boilerplate.setup import init_log

init_log()
app = Flask(__name__)
cors = CORS(app)


@app.route("/")
def welcome():
    return jsonify({"status": "welcome"})


@app.route("/search", methods=["POST"])
def search():
    """
    search (POST) to get discounts details

    args: (json)
        {
            "from": from location ex:"Santos",
            "to": destination name ex:"London",
            "commodity": type of merchandise ex:"Lithium",
            "date": date to export (0000-00-00) ex:"2022-10-31"
        }
    """

    json_input = request.get_json()
    _from = maesk_get_location(json_input["from"])
    sleep(.5)
    _to = maesk_get_location(json_input["to"])
    bearer_token = get_token()

    data = maesk_get_ship_price(
        bearer_token=bearer_token, 
        akamai_telemetry=akamai_telemetry,
        from_name=_from["city"],
        from_geoid=_from["maerskGeoLocationId"],
        to_name=_to["city"],
        to_geoid=_to["maerskGeoLocationId"],
        commodity=json_input["commodity"],
        send_date=json_input["date"]
    )

    return jsonify(data)

@app.errorhandler(Exception)
def handle_exception(e):

    e = str(e)
    try:
        e = json.loads(e)

        if e["code"] == 403:
            return jsonify({"error": e["code"], "message": e["message"]}), 403

        if e["code"] == 401:
            return jsonify({"error": e["code"], "message": e["message"]}), 401

        elif e["code"] == 404:
            return jsonify({"error": e["code"], "message": e["message"]}), 404

        return jsonify({"error": "internal server error"}), 500
    except Exception:
        return jsonify({"error": "internal server error"}), 500

if __name__ == "__main__":
    app.run()
