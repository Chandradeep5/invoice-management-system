
import os
import time

from werkzeug.utils import secure_filename
from datetime import datetime
from utils.file_handler import read_file
from utils.data_cleaner import clean_invoice_records

from utils.chunk_processor import (
    process_csv_in_chunks
)

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

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

def process_uploaded_file(file):

    try:

        start_time = time.time()

        # Secure filename
        filename = secure_filename(file.filename)

        # Get extension
        file_extension = os.path.splitext(
            filename
        )[1].lower()

        # Validate file
        validate_file_extension(file_extension)
        validate_file_size(file)

        # Save file
        file_path = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        file.save(file_path)

        # Existing invoice IDs
        existing_invoice_ids = {

            invoice["invoice_id"]

            for invoice in invoices_collection.find(
                {},
                {"invoice_id": 1}
            )
        }

        total_records = 0
        cleaned_count = 0
        inserted_count = 0

        # CSV Chunk Processing
        if file_extension == ".csv":

            for chunk in process_csv_in_chunks(
                file_path,
                chunk_size=1000
            ):

                records = chunk.to_dict(
                    orient="records"
                )

                total_records += len(records)

                cleaned_records = (
                    clean_invoice_records(
                        records
                    )
                )

                cleaned_count += len(
                    cleaned_records
                )

                new_records = [

                    record

                    for record in cleaned_records

                    if record["invoice_id"]
                    not in existing_invoice_ids
                ]

                if new_records:

                    result = (
                        invoices_collection.insert_many(
                            new_records,
                            ordered=False
                        )
                    )

                    inserted_count += len(
                        result.inserted_ids
                    )

                    # Update existing IDs set
                    for record in new_records:

                        existing_invoice_ids.add(
                            record["invoice_id"]
                        )

        else:

            df = read_file(
                file_path,
                file_extension
            )

            records = df.to_dict(
                orient="records"
            )

            total_records = len(records)

            cleaned_records = (
                clean_invoice_records(
                    records
                )
            )

            cleaned_count = len(
                cleaned_records
            )

            new_records = [

                record

                for record in cleaned_records

                if record["invoice_id"]
                not in existing_invoice_ids
            ]

            if new_records:

                result = (
                    invoices_collection.insert_many(
                        new_records,
                        ordered=False
                    )
                )

                inserted_count = len(
                    result.inserted_ids
                )

        processing_time = round(
            time.time() - start_time,
            2
        )

        logger.info(
            f"{inserted_count} invoices inserted successfully in {processing_time} seconds"
        )

        upload_log = {

            "file_name": filename,

            "uploaded_at":
                datetime.now(),

            "total_records":
                total_records,

            "cleaned_records":
                cleaned_count,

            "inserted_records":
                inserted_count,

            "skipped_records":
                total_records - inserted_count,

            "processing_time_seconds":
                processing_time,

            "status":
                "Success"
        }

        create_upload_log(
            upload_log
        )

        return {

            "total_uploaded_records":
                total_records,

            "cleaned_records":
                cleaned_count,

            "inserted_records":
                inserted_count,

            "skipped_records":
                total_records - inserted_count,

            "processing_time_seconds":
                processing_time
        }

    except Exception as error:

        logger.error(
            f"Upload failed: {str(error)}"
        )

        raise error
