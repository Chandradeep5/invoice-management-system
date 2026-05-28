
import os

from werkzeug.utils import secure_filename
from datetime import datetime
from utils.file_handler import read_file
from utils.data_cleaner import clean_invoice_records

from utils.validators import (
    validate_file_extension,
    validate_file_size
)



from services.upload_log_service import (
    create_upload_log
)
from database.db import invoices_collection

from utils.logger import logger


UPLOAD_FOLDER = "uploads"


def process_uploaded_file(file):

    try:

        # Secure filename
        filename = secure_filename(file.filename)

        # Get extension
        file_extension = os.path.splitext(
            filename
        )[1].lower()

        # Validate file extension
        validate_file_extension(file_extension)

        # Validate file size
        validate_file_size(file)

        # Create upload path
        file_path = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        # Save file
        file.save(file_path)

        # Read uploaded file
        df = read_file(
            file_path,
            file_extension
        )

        # Convert dataframe to records
        records = df.to_dict(
            orient="records"
        )

        # Clean records
        cleaned_records = clean_invoice_records(
            records
        )

        # Existing invoice IDs
        existing_invoice_ids = set()

        for invoice in invoices_collection.find(
            {},
            {"invoice_id": 1}
        ):

            existing_invoice_ids.add(
                invoice["invoice_id"]
            )

        # Remove duplicate invoices
        new_records = [

            record

            for record in cleaned_records

            if record["invoice_id"]
            not in existing_invoice_ids
        ]

        # Insert records
        inserted_count = 0

        if new_records:

            result = invoices_collection.insert_many(
                new_records
            )

            inserted_count = len(
                result.inserted_ids
            )

            logger.info(
                f"{inserted_count} invoices inserted successfully"
            )

            # Create upload log
            upload_log = {

                "file_name": filename,

                "uploaded_at":
                    datetime.now(),

                "inserted_records":
                    inserted_count,

                "skipped_records":
                    len(records) - inserted_count,

                "status": "Success"
            }

            create_upload_log(
                upload_log
            )

        return {

            "total_uploaded_records": len(records),

            "cleaned_records": len(cleaned_records),

            "inserted_records": inserted_count,

            "skipped_records":
                len(records) - inserted_count
        }

    except Exception as error:

        logger.error(str(error))

        raise error
