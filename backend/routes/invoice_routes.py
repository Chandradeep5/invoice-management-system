
from flask import Blueprint, jsonify, request
import time
from services.invoice_service import (
    get_all_invoices,
    get_total_invoice_count,
    get_invoice_by_id,
    filter_invoices,
    search_invoices,
    sort_invoices,
    paginate_invoices,
    update_invoice,
    delete_invoice,
    delete_all_invoices,
    get_total_invoice_count
)


invoice_bp = Blueprint("invoice_bp", __name__)


# Fetch all invoices
@invoice_bp.route("/api/invoices", methods=["GET"])
def fetch_all_invoices():
    """
    Fetch All Invoices
    ---
    tags:
        - Invoice

    parameters:
        - name: page
          in: query
          type: integer
          default: 1

        - name: limit
          in: query
          type: integer
          default: 20
          
    responses:
        200:
            description: List of all invoices
    """

    try:

        page = int(
            request.args.get("page",1)
        )

        limit = int(
            request.args.get("limit",20)
        )
        invoices = get_all_invoices(
            page,
            limit
        )
        total_records = get_total_invoice_count()

        return jsonify({
            "success": True,

            "page": page,

            "limit": limit,

            "records_returned": len(invoices),

            "total_records": total_records,

            "data": invoices
        })

    except Exception as error:

        return jsonify({
            "success": False,
            "message": str(error)
        }), 500


# Count invoices
@invoice_bp.route("/api/invoices/count", methods=["GET"])
def count_invoices():
    """
    Count Invoices
    ---
    tags:
        - Invoice

    responses:
      200:
        description: Total invoice count
    """

    try:

        total_records = get_total_invoice_count()

        return jsonify({
            "success": True,
            "total_invoices": total_records
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
    Search Invoice By ID
    ---
    tags:
        - Invoice
        
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
            "message": "Invoice fetched successfully",

            "invoice": {
                "invoice_id": invoice.get("invoice_id"),
                "invoice_date": invoice.get("invoice_date"),
                "due_date": invoice.get("due_date")
            },

            "customer": {
                "customer_name": invoice.get("customer_name"),
                "customer_email": invoice.get("customer_email"),
                "customer_phone": invoice.get("customer_phone")
            },

            "vendor": {
                "vendor_name": invoice.get("vendor_name"),
                "gst_number": invoice.get("gst_number")
            },

            "payment": {
                "amount": invoice.get("amount"),
                "tax_amount": invoice.get("tax_amount"),
                "total_amount": invoice.get("total_amount"),
                "payment_status": invoice.get("payment_status"),
                "payment_method": invoice.get("payment_method")
            },

            "business": {
                "category": invoice.get("category"),
                "currency": invoice.get("currency"),
                "location": invoice.get("location")
            }
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
    tags:
        - Invoice
        
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

      - name: start_date
        in: query
        type: string

      - name: end_date
        in: query
        type: string

      - name: due_before
        in: query
        type: string


    responses:
      200:
        description: Filtered invoices
    """

    try:

        filters = {
            "location": request.args.get("location"),
            "payment_status": request.args.get("payment_status"),
            "min_amount": request.args.get("min_amount"),
            "max_amount": request.args.get("max_amount"),
            "start_date": request.args.get("start_date"),
            "end_date": request.args.get("end_date"),
            "due_before": request.args.get("due_before")

        }

        invoices = filter_invoices(filters)

        return jsonify({
            "success": True,
            "records_found": len(invoices),
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
    tags:
        - Invoice
        
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
            "keyword":keyword,
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
    tags:
        - Invoice

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

        start_time = time.time()

        field = request.args.get("field")
        order = request.args.get("order", "asc")

        allowed_fields = [
            "invoice_id",
            "customer_name",
            "amount",
            "tax_amount",
            "total_amount",
            "invoice_date",
            "due_date",
            "location",
            "payment_status"
        ]

        if not field:
            return jsonify({
                "success": False,
                "message": "Field is required"
            }), 400

        if field not in allowed_fields:
            return jsonify({
                "success": False,
                "message": "Invalid sort field"
            }), 400

        if order not in ["asc", "desc"]:
            return jsonify({
                "success": False,
                "message": "Order must be asc or desc"
            }), 400

        invoices = sort_invoices(field, order)

        execution_time = round(
            time.time() - start_time,
            3
        )

        return jsonify({
            "success": True,
            "sorted_by": field,
            "sort_order": order,
            "records_found": len(invoices),
            "execution_time_seconds": execution_time,
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
    tags:
        - Invoice
        
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
        if page < 1:
            page = 1

        if limit < 1 or limit > 100:
            limit = 20

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

# Update invoice
@invoice_bp.route(
    "/api/invoices/<invoice_id>",
    methods=["PUT"]
)
def update_invoice_data(invoice_id):
    """
    Update Invoice
    ---
    tags:
        - Invoice
        
    parameters:
      - name: invoice_id
        in: path
        type: string
        required: true

    responses:
      200:
        description: Invoice updated successfully
    """

    try:

        updated_data = request.json

        modified_count = update_invoice(
            invoice_id,
            updated_data
        )

        if modified_count == 0:

            return jsonify({
                "success": False,
                "message": "Invoice not found"
            }), 404

        return jsonify({
            "success": True,
            "message": "Invoice updated successfully"
        })

    except Exception as error:

        return jsonify({
            "success": False,
            "message": str(error)
        }), 500
    
# Delete invoice
@invoice_bp.route(
    "/api/invoices/<invoice_id>",
    methods=["DELETE"]
)
def delete_invoice_data(invoice_id):
    """
    Delete Invoice
    ---
    tags:
        - Delete Invoice
        
    parameters:
      - name: invoice_id
        in: path
        type: string
        required: true

    responses:
      200:
        description: Invoice deleted successfully
    """

    try:

        deleted_count = delete_invoice(
            invoice_id
        )

        if deleted_count == 0:

            return jsonify({
                "success": False,
                "message": "Invoice not found"
            }), 404

        return jsonify({
            "success": True,
            "message": "Invoice deleted successfully"
        })

    except Exception as error:

        return jsonify({
            "success": False,
            "message": str(error)
        }), 500


# Delete all invoices
@invoice_bp.route(
    "/api/invoices",
    methods=["DELETE"]
)
def delete_all_invoice_data():
    """
    Delete All Invoices
    ---
    tags:
        - Invoice

    parameters:
        - name: confirm
          in: query
          type: string
          required: true
          default: YES

    responses:
        200:
            description: All invoices deleted successfully
    """

    try:

        confirm = request.args.get("confirm")

        if confirm != "YES":

            return jsonify({
                "success": False,
                "message": "Pass confirm=YES to delete all invoices"
            }), 400

        deleted_count = delete_all_invoices()

        return jsonify({
            "success": True,
            "message": "All invoices deleted successfully",
            "deleted_records": deleted_count
        })

    except Exception as error:

        return jsonify({
            "success": False,
            "message": str(error)
        }), 500