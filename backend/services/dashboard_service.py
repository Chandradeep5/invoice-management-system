from database.db import invoices_collection


# Dashboard statistics
def get_dashboard_stats():

    total_invoices = invoices_collection.count_documents({})

    total_revenue_pipeline = [
        {
            "$group": {
                "_id": None,
                "total_revenue": {
                    "$sum": "$total_amount"
                }
            }
        }
    ]

    revenue_result = list(
        invoices_collection.aggregate(total_revenue_pipeline)
    )

    total_revenue = 0

    if revenue_result:
        total_revenue = revenue_result[0]["total_revenue"]

    paid_invoices = invoices_collection.count_documents({
        "payment_status": "Paid"
    })

    pending_invoices = invoices_collection.count_documents({
        "payment_status": "Pending"
    })

    return {
        "total_invoices": total_invoices,
        "total_revenue": total_revenue,
        "paid_invoices": paid_invoices,
        "pending_invoices": pending_invoices
    }


# Revenue by location
def get_revenue_by_location():

    pipeline = [
        {
            "$group": {
                "_id": "$location",
                "total_revenue": {
                    "$sum": "$total_amount"
                }
            }
        }
    ]

    result = list(
        invoices_collection.aggregate(pipeline)
    )

    return result


# Payment summary
def get_payment_summary():

    pipeline = [
        {
            "$group": {
                "_id": "$payment_status",
                "count": {
                    "$sum": 1
                }
            }
        }
    ]

    result = list(
        invoices_collection.aggregate(pipeline)
    )

    return result
