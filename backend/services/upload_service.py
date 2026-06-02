
import os
import time

from werkzeug.utils import secure_filename
from datetime import datetime
from utils.file_handler import read_file
from utils.data_cleaner import clean_invoice_records

from pymongo.errors import BulkWriteError

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



        total_records = 0
        cleaned_count = 0
        inserted_count = 0

        # CSV Chunk Processing
        if file_extension == ".csv":

            for chunk in process_csv_in_chunks(
                file_path,
                chunk_size=10000
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

                new_records = cleaned_records

                if new_records:

                    try:

                        result = invoices_collection.insert_many(
                            new_records,
                            ordered=False
                        )

                        inserted_count += len(
                            result.inserted_ids
                        )

                    except BulkWriteError as error:

                        inserted_count += (
                            error.details.get(
                                "nInserted",
                                0
                            )
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

            new_records = cleaned_records

            if new_records:

                try:

                    result = invoices_collection.insert_many(
                        new_records,
                        ordered=False
                    )

                    inserted_count += len(
                        result.inserted_ids
                    )

                except BulkWriteError as error:

                    inserted_count += (
                        error.details.get(
                            "nInserted",
                            0
                        )
                    )

        processing_time = round(
            time.time() - start_time,
            2
        )

        records_per_second = 0

        if processing_time > 0:

            records_per_second = round(
                total_records / processing_time,
                2
            )

        logger.info(
            f"{inserted_count} invoices inserted in "
            f"{processing_time} seconds "
            f"({records_per_second} records/sec)"
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

            "duplicate_records":
                cleaned_records - inserted_count,

            "records_per_second":
                records_per_second,

            "processing_time_seconds":
                processing_time,

            "status":
                "Success"
        }

        create_upload_log(
            upload_log
        )

    

        return {
            "file_name": filename,

            "total_uploaded_records":
                total_records,

            "cleaned_records":
                cleaned_count,

            "inserted_records":
                inserted_count,

            "duplicate_records":
                cleaned_records - inserted_count,

            "records_per_second":
                records_per_second,

            "processing_time_seconds":
                processing_time
        }

    except Exception as error:

        logger.error(
            f"Upload failed: {str(error)}"
        )

        raise error


    finally:
            

            if os.path.exists(file_path):

                os.remove(file_path)