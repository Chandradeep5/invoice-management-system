
from flask import Flask
from flasgger import Swagger
import os
from routes.upload_routes import upload_bp
from routes.invoice_routes import invoice_bp
from routes.dashboard_routes import dashboard_bp
from routes.health_routes import health_bp
from routes.export_routes import export_bp
from routes.upload_log_routes import upload_log_bp


# Create Flask App
app = Flask(__name__)

os.makedirs(
    "uploads",
    exist_ok=True
)

os.makedirs(
    "exports",
    exist_ok=True
)

os.makedirs(
    "logs",
    exist_ok=True
)

# Prevent JSON keys from being sorted
app.config["JSON_SORT_KEYS"] = False

# Allow large file uploads (100 MB)
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024

# Swagger Configuration
swagger = Swagger(app)


# Register Blueprints
app.register_blueprint(upload_bp)
app.register_blueprint(invoice_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(export_bp)
app.register_blueprint(health_bp)
app.register_blueprint(upload_log_bp)


@app.route("/")
def home():
    """
    Home API
    ---
    responses:
      200:
        description: API running successfully
    """

    return {
        "success": True,
        "message": "Invoice Management System API Running"
    }


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
