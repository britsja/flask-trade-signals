from flask import Blueprint, request, jsonify
import requests

def fetch_pagespeed_report(target_site: str):
  api_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
  query_parameters = {
    "url": target_site,
    "category": "performance"
  }
  print(f"Dispatched outgoing request to Google API for {target_site}")

  try:
    response = requests.get(api_url, params=query_parameters, timeout=45)
    response.raise_for_status()
    data = response.json()
    return data
  except requests.exceptions.RequestException as e:
    print(f"External API Error: {e}")
    return None

def extract_lighthouse_score(api_response: dict):
  if not api_response:
    return "No data to analyze"

  lighthouse_result = api_response.get("lighthouseResult", {})
  categories = lighthouse_result.get("categories", {})
  performance = categories.get("performance", {})
  score = performance.get("score")

  if score is not None:
    return f"Core performance score is: {score * 100}%"
  return "Performance score field is missing from API payload"

shopify_bp = Blueprint("shopify", __name__)

@shopify_bp.route("/audit", methods=["POST"])
def receive_audit_request():
  data = request.get_json()

  if not data or "target_url" not in data:
    return jsonify({"error": "Missing target_url parameter"}), 400

  page_speed_url =  data['target_url']
 
  print(f"Received audit request for store: {page_speed_url}")

  api_response = fetch_pagespeed_report(page_speed_url)

  page_speed_score = extract_lighthouse_score(api_response)  

  return jsonify({
    "status": "completed",
    "target_url": page_speed_url,
    "metrics": {
      "performance_score": page_speed_score
    }
  }), 200
