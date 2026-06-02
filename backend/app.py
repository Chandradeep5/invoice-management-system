
from flask import Flask
from flasgger import Swagger
import os
from flask import redirect

from flask import render_template
from flask import render_template
from routes.upload_routes import upload_bp
from routes.invoice_routes import invoice_bp
from routes.dashboard_routes import dashboard_bp
from routes.health_routes import health_bp
from routes.export_routes import export_bp
from routes.upload_log_routes import upload_log_bp


# Create Flask App
app = Flask(__name__)

# Create folders if not exist
os.makedirs("uploads", exist_ok=True)
os.makedirs("exports", exist_ok=True)
os.makedirs("logs", exist_ok=True)

# Flask Config
app.config["JSON_SORT_KEYS"] = False
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024

# Swagger Template
swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Invoice Management System API",
        "description": """
        Bulk Upload, Search, Filter, Dashboard Analytics,
        Export and Upload History APIs.
        """,
        "version": "1.0.0"
    }
}

# Swagger Configuration
swagger = Swagger(
    app,
    template=swagger_template
)

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

@app.route("/update-invoice")
def update_invoice_page():

    return render_template(
        "update_invoice.html"
    )

@app.route("/api/ui/update-invoice")
def update_invoice_ui():
    """
    Update Invoice UI
    ---
    tags:
      - UI Pages

    responses:
      302:
        description: Redirect to Update Invoice Page
    """

    return redirect("/update-invoice")

@app.route("/portal")
def portal():

    return """
    <h1>Invoice Management System</h1>

    <br>

    <a href='/apidocs'>
        Swagger APIs
    </a>

    <br><br>

    <a href='/update-invoice'>
        Update Invoice Page
    </a>
    """

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
