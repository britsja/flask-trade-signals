from flask import Blueprint, request, jsonify
from pydantic import BaseModel, Field, ValidationError
from typing import Literal

trading_bp = Blueprint("trading", __name__)

class TradingWebHook(BaseModel):
    ticker: str = Field(pattern=r"^[A-Z]+$")
    action: Literal["BUY", "SELL"]
    price: float = Field(gt=0)

@trading_bp.route("/webhook", methods=["POST"])
def receive_trade_request():  

  data = request.get_json()

  try:
    validated_trade = TradingWebHook(**data)
  except ValidationError as e:
    return jsonify({"error": e.errors()}), 400  

  print(f"Executing trade")
  def execute_trade(validated_trade: TradingWebHook):
    return f"{validated_trade.action} executed for {validated_trade.ticker} at {validated_trade.price}"

  return execute_trade(validated_trade), 202

