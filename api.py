from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import subprocess
import tempfile
import os
import base64
import logging
from lambda_function import lambda_handler
app = Flask(__name__)
CORS(app, origins=[r"https?://(\w+\.)*greicodex\.com"])

@app.route("/api", methods=["POST"])
def parse_gs1():
    try:
        data = request.get_data()
        logging.warning("Got data: %s" % data)
        output=lambda_handler({ "body": data },{})
        return app.response_class( response=output.get('body'),status=output.get('statusCode'), mimetype='application/json')
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Failed to generate process", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "An error occurred", "details": str(e)}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
