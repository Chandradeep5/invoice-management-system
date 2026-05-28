
from flask import Flask
from flasgger import Swagger

from routes.upload_routes import upload_bp
from routes.invoice_routes import invoice_bp
from routes.dashboard_routes import dashboard_bp


app = Flask(__name__)

swagger = Swagger(app)

# Register blueprints
app.register_blueprint(upload_bp)

# Register invoice blueprint 
app.register_blueprint(invoice_bp)

# Register dashboard blueprint
app.register_blueprint(dashboard_bp)


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
        "message": "Invoice Management System API Running"
    }

if __name__ == "__main__":
    app.run(debug=True)