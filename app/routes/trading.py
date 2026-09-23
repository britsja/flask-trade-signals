from flask import Blueprint, request, jsonify

trading_bp = Blueprint("trading", __name__)

@trading_bp.route("/webhook", method=["POST"])
def receive_trade_request():
  data = request.get_json()
  if not data or "target_url" not in data:
    return jsonify({"error": "Missing target_url parameter"}), 400

  print(f"Executing trade")

  return jsonify({
    "status": "executed",
    "message": "completed"
  }), 202

