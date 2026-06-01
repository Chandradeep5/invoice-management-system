
from flask import Blueprint, jsonify

health_bp = Blueprint(
    "health_bp",
    __name__
)


@health_bp.route(
    "/api/health",
    methods=["GET"]
)
def health_check():
    """
    Health Check API
    ---
    tags:
        - Health 
    responses:
      200:
        description: Server health check
    """

    return jsonify({
        "success": True,
        "message": "Server running successfully"
    })
