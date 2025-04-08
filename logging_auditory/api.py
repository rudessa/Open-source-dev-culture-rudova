import logging
from flask import Flask, request, jsonify

FORMATTER_STRING = "%(asctime)s — %(name)s — %(levelname)s — %(message)s"
FORMATTER = logging.Formatter(FORMATTER_STRING)

app = Flask(__name__)



@app.route("/log", methods=["POST"])
def receive_log():
    """
    Receives and prints critical logs sent via HTTP.
    """
    log_data = request.get_json()
    print("Received Critical Log:", log_data)
    return jsonify({"status": "received"}), 200

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)