
from flask import jsonify


# Success response
def success_response(
    message,
    data=None,
    status_code=200
):

    return jsonify({
        "success": True,
        "message": message,
        "data": data
    }), status_code


# Error response
def error_response(
    message,
    status_code=500
):

    return jsonify({
        "success": False,
        "message": message
    }), status_code
