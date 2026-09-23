from flask import Blueprint, request, jsonify

shopify_bp = Blueprint("shopify", __name__)

@shopify_bp.route("/audit", methods=["POST"])
def receive_audit_request():
  data = request.get_json()

  if not data or "target_url" not in data:
    return jsonify({"error": "Missing target_url parameter"}), 400

  print(f"Received audit request for store: {data['target_url']}")

  return jsonify({
    "status": "accepted",
    "message": "Audit processing job initiated"
  }), 202
