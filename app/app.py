"""PyCalc — a simple calculator exposed as a REST API, documented with Swagger."""

from flask import Flask, jsonify, render_template, request
from flasgger import Swagger

from calculator import add, divide, multiply, subtract

app = Flask(__name__)
app.config["SWAGGER"] = {
    "title": "PyCalc API",
    "uiversion": 3,
}
swagger = Swagger(app)

OPERATIONS = {
    "add": add,
    "subtract": subtract,
    "multiply": multiply,
    "divide": divide,
}


@app.route("/")
def home():
    """Render the calculator page shown in the browser."""
    return render_template("index.html")


@app.route("/health")
def health():
    """Health check endpoint used by Kubernetes probes.
    ---
    responses:
      200:
        description: The service is healthy.
    """
    return jsonify(status="ok")


@app.route("/api/calculate", methods=["POST"])
def calculate():
    """Perform a calculation.
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            operation:
              type: string
              enum: [add, subtract, multiply, divide]
              example: add
            a:
              type: number
              example: 4
            b:
              type: number
              example: 2
    responses:
      200:
        description: The calculation result.
      400:
        description: Invalid input.
    """
    data = request.get_json(silent=True) or {}
    operation = data.get("operation")
    a = data.get("a")
    b = data.get("b")

    if operation not in OPERATIONS:
        return jsonify(error=f"Unknown operation '{operation}'"), 400
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        return jsonify(error="'a' and 'b' must be numbers"), 400

    try:
        result = OPERATIONS[operation](a, b)
    except ValueError as exc:
        return jsonify(error=str(exc)), 400

    return jsonify(operation=operation, a=a, b=b, result=result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)