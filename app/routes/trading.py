from flask import Blueprint, request, jsonify
from pydantic import BaseModel, Field, ValidationError
from typing import Literal

trading_bp = Blueprint("trading", __name__)

class TradingWebHook(BaseModel):
    ticker: str = Field(pattern=r"^[A-Z]+$")
    action: Literal["BUY", "SELL"]
    price: float = Field(gt=0)

def execute_trade(validated_trade: TradingWebHook) -> str:
    return f"{validated_trade.action} executed for {validated_trade.ticker} at {validated_trade.price}"

@trading_bp.route("/webhook", methods=["POST"])
def receive_trade_request():
  data = request.get_json()

  if not data:
     return jsonify({"error", "No JSON payload received"}), 400

  try:
    validated_trade = TradingWebHook(**data)
  except ValidationError as e:
    return jsonify({"error": e.errors()}), 400  

  print(f"Signal validated for {validated_trade.ticker}. Dispatching execution...")

  execution_result = execute_trade(validated_trade)

  return jsonify({
     "status": "completed successfully",
     "message": execution_result
  }), 202


