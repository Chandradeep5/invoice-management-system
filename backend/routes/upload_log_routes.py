from flask import Blueprint, jsonify

from services.upload_log_service import (
    get_upload_logs,
    get_latest_upload_log
)

upload_log_bp = Blueprint(
    "upload_log_bp",
    __name__
)


# Fetch all upload logs
@upload_log_bp.route(
    "/api/upload-logs",
    methods=["GET"]
)
def fetch_upload_logs():
    """
    Fetch Upload Logs
    ---
    tags:
        - Upload logs
    responses:
      200:
        description: Upload logs fetched successfully
    """

    try:

        logs = get_upload_logs()

        return jsonify({
            "success": True,
            "total_records": len(logs),
            "data": logs
        })

    except Exception as error:

        return jsonify({
            "success": False,
            "message": str(error)
        }), 500


# Fetch latest upload log
@upload_log_bp.route(
    "/api/upload-logs/latest",
    methods=["GET"]
)
def fetch_latest_upload_log():
    """
    Fetch Latest Upload Log
    ---
    tags:
        - Upload logs
    responses:
      200:
        description: Latest upload log
    """

    try:

        log = get_latest_upload_log()

        return jsonify({
            "success": True,
            "data": log
        })

    except Exception as error:

        return jsonify({
            "success": False,
            "message": str(error)
        }), 500
