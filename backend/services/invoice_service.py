
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
