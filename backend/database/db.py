
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Read Environment Variables
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

# Validation
if not MONGO_URI:
    raise Exception(
        "MONGO_URI not found in .env file"
    )

if not DATABASE_NAME:
    raise Exception(
        "DATABASE_NAME not found in .env file"
    )

# Create Mongo Client
client = MongoClient(MONGO_URI)

# Select Database
db = client[DATABASE_NAME]

# Collections
invoices_collection = db["invoices"]
upload_logs_collection = db["upload_logs"]

# Indexes
invoices_collection.create_index(
    "invoice_id",
    unique=True
)

invoices_collection.create_index(
    "customer_name"
)

invoices_collection.create_index(
    "location"
)

invoices_collection.create_index(
    "payment_status"
)

invoices_collection.create_index(
    "invoice_date"
)