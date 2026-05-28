
import os
from werkzeug.utils import secure_filename

from utils.file_handler import read_file
from utils.validators import validate_file_extension
from utils.data_cleaner import clean_invoice_records

from database.db import invoices_collection

UPLOAD_FOLDER = "uploads"

def process_uploaded_file(file):

    # Secure filename
    filename = secure_filename(file.filename)

    # Get extension
    file_extension = os.path.splitext(filename)[1].lower()

    # Validate extension
    validate_file_extension(file_extension)

    # Save file
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    file.save(file_path)

    # Read file
    df = read_file(file_path, file_extension)

    # Convert dataframe to records
    records = df.to_dict(orient="records")

    # Clean records
    cleaned_records = clean_invoice_records(records)

    # Check existing invoice IDs in DB
    existing_invoice_ids = set()

    for invoice in invoices_collection.find(
        {},
        {"invoice_id": 1}
    ):
        existing_invoice_ids.add(invoice["invoice_id"])

    # Remove already existing invoices
    new_records = [
        record for record in cleaned_records
        if record["invoice_id"] not in existing_invoice_ids
    ]

    # Insert records
    inserted_count = 0

    if new_records:
        result = invoices_collection.insert_many(new_records)
        inserted_count = len(result.inserted_ids)

    return {
        "total_uploaded_records": len(records),
        "cleaned_records": len(cleaned_records),
        "inserted_records": inserted_count,
        "skipped_records": len(records) - inserted_count
    }
