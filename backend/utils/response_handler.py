
from flask import jsonify
from datetime import datetime


def success_response(
    message,
    data=None,
    metadata=None,
    status_code=200
):

    return jsonify({

        "success": True,

        "message": message,

        "timestamp":
            datetime.utcnow().isoformat(),

        "metadata":
            metadata or {},

        "data":
            data

    }), status_code


def error_response(
    message,
    status_code=500
):

    return jsonify({

        "success": False,

        "message": message,

        "timestamp":
            datetime.utcnow().isoformat()

    }), status_code
