from flask import Blueprint, jsonify

from services.invoice_service import (
    get_all_invoices,
    get_invoice_by_id
)

invoice_bp = Blueprint("invoice_bp", __name__)


# Fetch all invoices
@invoice_bp.route("/api/invoices", methods=["GET"])
def fetch_all_invoices():
    """
    Fetch All Invoices
    ---
    responses:
      200:
        description: List of all invoices
    """

    try:

        invoices = get_all_invoices()

        return jsonify({
            "success": True,
            "total_records": len(invoices),
            "data": invoices
        })

    except Exception as error:

        return jsonify({
            "success": False,
            "message": str(error)
        }), 500


# Fetch invoice by invoice ID
@invoice_bp.route("/api/invoices/<invoice_id>", methods=["GET"])
def fetch_invoice(invoice_id):
    """
    Fetch Invoice By ID
    ---
    parameters:
      - name: invoice_id
        in: path
        type: string
        required: true

    responses:
      200:
        description: Invoice fetched successfully
      404:
        description: Invoice not found
    """

    try:

        invoice = get_invoice_by_id(invoice_id)

        if not invoice:
            return jsonify({
                "success": False,
                "message": "Invoice not found"
            }), 404

        return jsonify({
            "success": True,
            "data": invoice
        })

    except Exception as error:

        return jsonify({
            "success": False,
            "message": str(error)
        }), 500
