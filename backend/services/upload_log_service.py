
from datetime import datetime

from database.db import (
    upload_logs_collection
)


# Create upload log
def create_upload_log(log_data):

    upload_logs_collection.insert_one(
        log_data
    )


# Fetch all upload logs
def get_upload_logs():

    logs = list(
        upload_logs_collection.find(
            {},
            {"_id": 0}
        ).sort("uploaded_at", -1)
    )

    return logs


# Fetch latest upload log
def get_latest_upload_log():

    log = upload_logs_collection.find_one(
        {},
        {"_id": 0},
        sort=[("uploaded_at", -1)]
    )

    return log