
from database.db import invoices_collection


# Fetch all invoices
def get_all_invoices():

    invoices = list(
        invoices_collection.find({}, {"_id": 0})
    )

    return invoices


# Fetch invoice by ID
def get_invoice_by_id(invoice_id):

    invoice = invoices_collection.find_one(
        {"invoice_id": invoice_id},
        {"_id": 0}
    )

    return invoice


# Filter invoices
def filter_invoices(filters):

    query = {}

    # Filter by location
    if filters.get("location"):
        query["location"] = filters["location"]

    # Filter by payment status
    if filters.get("payment_status"):
        query["payment_status"] = filters["payment_status"]

    # Filter by minimum amount
    if filters.get("min_amount"):

        query["amount"] = {
            "$gte": float(filters["min_amount"])
        }

    # Filter by maximum amount
    if filters.get("max_amount"):

        if "amount" not in query:
            query["amount"] = {}

        query["amount"]["$lte"] = float(filters["max_amount"])

    # Filter by invoice date range
    if filters.get("start_date") and filters.get("end_date"):

        query["invoice_date"] = {
            "$gte": filters["start_date"],
            "$lte": filters["end_date"]
        }

    # Filter by due date
    if filters.get("due_before"):

        query["due_date"] = {
            "$lte": filters["due_before"]
        }


    invoices = list(
        invoices_collection.find(query, {"_id": 0})
    )

    return invoices


# Search invoices
def search_invoices(keyword):

    query = {
        "$or": [
            {
                "invoice_id": {
                    "$regex": keyword,
                    "$options": "i"
                }
            },
            {
                "customer_name": {
                    "$regex": keyword,
                    "$options": "i"
                }
            }
        ]
    }

    invoices = list(
        invoices_collection.find(query, {"_id": 0})
    )

    return invoices


# Sort invoices
def sort_invoices(field, order):

    sort_order = 1

    if order == "desc":
        sort_order = -1

    invoices = list(
        invoices_collection.find({}, {"_id": 0})
        .sort(field, sort_order)
    )

    return invoices


# Paginate invoices
def paginate_invoices(page, limit):

    skip = (page - 1) * limit

    invoices = list(
        invoices_collection.find({}, {"_id": 0})
        .skip(skip)
        .limit(limit)
    )

    return invoices

# Update invoice
def update_invoice(invoice_id, updated_data):

    result = invoices_collection.update_one(
        {"invoice_id": invoice_id},
        {
            "$set": updated_data
        }
    )

    return result.modified_count

# Delete invoice
def delete_invoice(invoice_id):

    result = invoices_collection.delete_one(
        {"invoice_id": invoice_id}
    )

    return result.deleted_count

