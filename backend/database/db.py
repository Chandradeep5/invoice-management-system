
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

upload_logs_collection = db["upload_logs"]

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