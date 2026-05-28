
from flask import Flask
from flasgger import Swagger
from database.db import db

app = Flask(__name__)

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

@app.route("/test-db")
def test_db():
    """
    Test MongoDB Connection
    ---
    responses:
      200:
        description: MongoDB connection successful
    """
    return {
        "message": "MongoDB connected successfully"
    }

if __name__ == "__main__":
    app.run(debug=True)
