from flask import Flask

def create_app() -> Flask:
  app = Flask(__name__)
  from app.routes.shopify import shopify_bp
  from app.routes.trading import trading_bp
  app.register_blueprint(shopify_bp, url_prefix="/api/v1/shopify")
  app.register_blueprint(trading_bp, url_prefix="/api/v1/trading")
  return app