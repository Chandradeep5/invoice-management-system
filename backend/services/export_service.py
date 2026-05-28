import pandas as pd

from database.db import invoices_collection


def export_invoices_to_csv():

    # Fetch invoices
    invoices = list(
        invoices_collection.find({}, {"_id": 0})
    )

    # Convert to dataframe
    df = pd.DataFrame(invoices)

    # Export path
    export_path = "exports/invoices_export.csv"

    # Create exports folder if not exists
    import os

    if not os.path.exists("exports"):
        os.makedirs("exports")

    # Save CSV
    df.to_csv(export_path, index=False)

    return export_path
