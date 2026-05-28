
from flask import Blueprint, jsonify, request

from services.invoice_service import (
    get_all_invoices,
    get_invoice_by_id,
    filter_invoices,
    search_invoices,
    sort_invoices,
    paginate_invoices
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


# Filter invoices
@invoice_bp.route("/api/invoices/filter", methods=["GET"])
def filter_invoice_data():
    """
    Filter Invoices
    ---
    parameters:
      - name: location
        in: query
        type: string

      - name: payment_status
        in: query
        type: string

      - name: min_amount
        in: query
        type: number

      - name: max_amount
        in: query
        type: number

    responses:
      200:
        description: Filtered invoices
    """

    try:

        filters = {
            "location": request.args.get("location"),
            "payment_status": request.args.get("payment_status"),
            "min_amount": request.args.get("min_amount"),
            "max_amount": request.args.get("max_amount")
        }

        invoices = filter_invoices(filters)

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

# Search invoices
@invoice_bp.route("/api/invoices/search", methods=["GET"])
def search_invoice_data():
    """
    Search Invoices
    ---
    parameters:
      - name: keyword
        in: query
        type: string
        required: true

    responses:
      200:
        description: Search results
    """

    try:

        keyword = request.args.get("keyword")

        if not keyword:
            return jsonify({
                "success": False,
                "message": "Keyword is required"
            }), 400

        invoices = search_invoices(keyword)

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

# Sort invoices
@invoice_bp.route("/api/invoices/sort", methods=["GET"])
def sort_invoice_data():
    """
    Sort Invoices
    ---
    parameters:
      - name: field
        in: query
        type: string
        required: true

      - name: order
        in: query
        type: string
        enum: [asc, desc]

    responses:
      200:
        description: Sorted invoices
    """

    try:

        field = request.args.get("field")
        order = request.args.get("order", "asc")

        if not field:
            return jsonify({
                "success": False,
                "message": "Field is required"
            }), 400

        invoices = sort_invoices(field, order)

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


# Paginate invoices
@invoice_bp.route("/api/invoices/paginate", methods=["GET"])
def paginate_invoice_data():
    """
    Paginate Invoices
    ---
    parameters:
      - name: page
        in: query
        type: integer

      - name: limit
        in: query
        type: integer

    responses:
      200:
        description: Paginated invoices
    """

    try:

        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))

        invoices = paginate_invoices(page, limit)

        return jsonify({
            "success": True,
            "page": page,
            "limit": limit,
            "total_records": len(invoices),
            "data": invoices
        })

    except Exception as error:

        return jsonify({
            "success": False,
            "message": str(error)
        }), 500
