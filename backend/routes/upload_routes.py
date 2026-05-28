

from flask import Blueprint, request, jsonify
from services.upload_service import process_uploaded_file

upload_bp = Blueprint("upload_bp", __name__)

@upload_bp.route("/api/upload", methods=["POST"])
def upload_file():
    """
    Upload Invoice File
    ---
    consumes:
      - multipart/form-data
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: Upload CSV, XLSX, or JSON file

    responses:
      200:
        description: File uploaded successfully
      400:
        description: Invalid request
    """

    try:

        # Check file exists
        if "file" not in request.files:
            return jsonify({
                "success": False,
                "message": "No file uploaded"
            }), 400

        file = request.files["file"]

        # Process uploaded file
        records = process_uploaded_file(file)

        return jsonify({
            "success": True,
            "message": "File processed successfully",
            "total_records": len(records),
            "data": records[:5]
        })

    except Exception as error:

        return jsonify({
            "success": False,
            "message": str(error)
        }), 500
