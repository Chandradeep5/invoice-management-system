
import os
from werkzeug.utils import secure_filename

from utils.file_handler import read_file
from utils.validators import validate_file_extension

UPLOAD_FOLDER = "uploads"

def process_uploaded_file(file):

    # Secure filename
    filename = secure_filename(file.filename)

    # Extract extension
    file_extension = os.path.splitext(filename)[1].lower()

    # Validate extension
    validate_file_extension(file_extension)

    # Create upload path
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    # Save file
    file.save(file_path)

    # Read file
    df = read_file(file_path, file_extension)

    # Convert dataframe to dictionary
    records = df.to_dict(orient="records")

    return records
