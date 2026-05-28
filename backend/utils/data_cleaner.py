
def clean_invoice_records(records):

    cleaned_records = []
    seen_invoice_ids = set()

    for record in records:

        # Remove spaces from keys
        record = {k.strip(): v for k, v in record.items()}

        # Required fields check
        required_fields = [ "invoice_id", "customer_name", "amount", "payment_status", "location", "invoice_date", "payment_method" ]

        missing_fields = [
            field for field in required_fields
            if field not in record or record[field] == ""
        ]

        if missing_fields:
            continue

        # Standardize invoice ID
        invoice_id = str(record["invoice_id"]).strip().upper()

        # Remove duplicate invoice IDs in uploaded file
        if invoice_id in seen_invoice_ids:
            continue

        seen_invoice_ids.add(invoice_id)

        record["invoice_id"] = invoice_id

        # Handle amount validation
        try:
            record["amount"] = float(record["amount"])
        except:
            continue

        # Handle missing payment status
        if not record.get("payment_status"):
            record["payment_status"] = "Pending"

        cleaned_records.append(record)

    return cleaned_records
