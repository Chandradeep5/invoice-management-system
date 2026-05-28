from flask import Blueprint, send_file, jsonify

from services.export_service import (
    export_invoices_to_csv
)

export_bp = Blueprint(
    "export_bp",
    __name__
)


@export_bp.route(
    "/api/export/csv",
    methods=["GET"]
)
def export_csv():
    """
    Export Invoices to CSV
    ---
    responses:
      200:
        description: CSV exported successfully
    """

    try:

        file_path = export_invoices_to_csv()

        return send_file(
            file_path,
            as_attachment=True
        )

    except Exception as error:

        return jsonify({
            "success": False,
            "message": str(error)
        }), 500
