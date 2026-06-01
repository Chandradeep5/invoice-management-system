from flask import Blueprint, jsonify

from services.dashboard_service import (
    get_dashboard_stats,
    get_revenue_by_location,
    get_payment_summary
)

dashboard_bp = Blueprint(
    "dashboard_bp",
    __name__
)


# Dashboard statistics
@dashboard_bp.route(
    "/api/dashboard/stats",
    methods=["GET"]
)
def dashboard_stats():
    """
    📊 Dashboard Statistics
    ---
    tags:
        - Dashboard
    responses:
      200:
        description: Dashboard statistics
    """

    try:

        stats = get_dashboard_stats()

        return jsonify({
            "success": True,
            "data": stats
        })

    except Exception as error:

        return jsonify({
            "success": False,
            "message": str(error)
        }), 500


# Revenue by location
@dashboard_bp.route(
    "/api/dashboard/revenue-by-location",
    methods=["GET"]
)
def revenue_by_location():
    """
    📊 Revenue By Location
    ---
    tags:
        - Dashboard
    responses:
      200:
        description: Revenue grouped by location
    """

    try:

        result = get_revenue_by_location()

        return jsonify({
            "success": True,
            "data": result
        })

    except Exception as error:

        return jsonify({
            "success": False,
            "message": str(error)
        }), 500


# Payment summary
@dashboard_bp.route(
    "/api/dashboard/payment-summary",
    methods=["GET"]
)
def payment_summary():
    """
    📊 Payment Summary
    ---
    tags:
        - Dashboard
    responses:
      200:
        description: Payment status summary
    """

    try:

        result = get_payment_summary()

        return jsonify({
            "success": True,
            "data": result
        })

    except Exception as error:

        return jsonify({
            "success": False,
            "message": str(error)
        }), 500
