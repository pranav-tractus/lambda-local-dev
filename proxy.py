import os
import json
import logging
import requests
from flask import Flask, request, jsonify

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

LAMBDA_PORT = int(os.environ["LAMBDA_PORT"])
PROXY_PORT = int(os.environ["PROXY_PORT"])
FUNCTION_NAME = os.environ.get("FUNCTION_NAME", "FunctionImp")
LAMBDA_URL = f"http://127.0.0.1:{LAMBDA_PORT}/2015-03-31/functions/{FUNCTION_NAME}/invocations"

app = Flask(__name__)


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization,X-Requested-With"
    return response


@app.route("/", methods=["OPTIONS"])
@app.route("/<path:path>", methods=["OPTIONS"])
def preflight(path=""):
    return "", 204


@app.route("/", methods=["POST", "GET", "PUT", "DELETE"])
@app.route("/<path:path>", methods=["POST", "GET", "PUT", "DELETE"])
def proxy(path=""):
    event = {
        "version": "2.0",
        "routeKey": "$default",
        "rawPath": f"/{path}" if path else "/",
        "rawQueryString": request.query_string.decode("utf-8") if request.query_string else "",
        "headers": dict(request.headers),
        "body": request.get_data(as_text=True) if request.data else None,
        "isBase64Encoded": False,
        "requestContext": {
            "accountId": "local",
            "apiId": "local",
            "domainName": "localhost",
            "domainPrefix": "local",
            "http": {
                "method": request.method,
                "path": f"/{path}" if path else "/",
                "protocol": "HTTP/1.1",
                "sourceIp": request.remote_addr,
                "userAgent": request.headers.get("User-Agent", ""),
            },
            "requestId": "proxy-request",
            "routeKey": "$default",
            "stage": "local",
            "time": request.headers.get("Date", ""),
            "timeEpoch": 0,
        },
    }

    try:
        response = requests.post(LAMBDA_URL, json=event, timeout=90)
        result = response.json()

        if "statusCode" in result:
            status_code = result.get("statusCode", 200)
            response_body = result.get("body", "")
            response_headers = result.get("headers", {})

            if isinstance(response_body, str):
                try:
                    response_body = json.loads(response_body)
                except json.JSONDecodeError:
                    pass

            flask_response = jsonify(response_body)
            flask_response.status_code = status_code
            for name, value in response_headers.items():
                if name.lower() not in ["content-length", "content-encoding"]:
                    flask_response.headers[name] = value
            return flask_response

        return jsonify(result), 200

    except requests.exceptions.Timeout:
        return jsonify({"error": "Request timed out"}), 504
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Lambda service not available"}), 503
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid response from Lambda service"}), 502
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({"error": f"Proxy error: {str(e)}"}), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "lambda_url": LAMBDA_URL, "proxy_port": PROXY_PORT})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PROXY_PORT, debug=False)
