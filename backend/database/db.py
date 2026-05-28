
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get Mongo URI
MONGO_URI = os.getenv("MONGO_URI")

# Create Mongo client
client = MongoClient(MONGO_URI)

# Select database
db = client[os.getenv("DATABASE_NAME")]

# Collections
invoices_collection = db["invoices"]
