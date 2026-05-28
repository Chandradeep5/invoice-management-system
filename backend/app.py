
from flask import Flask
from flasgger import Swagger

app = Flask(__name__)

# Swagger configuration
swagger = Swagger(app)

@app.route("/")
def home():
    """
    Home API
    ---
    responses:
      200:
        description: API is running successfully
    """
    return {
        "message": "Invoice Management System API Running"
    }

if __name__ == "__main__":
    app.run(debug=True)
