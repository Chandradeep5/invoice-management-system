
ALLOWED_EXTENSIONS = [".csv", ".xlsx", ".json"]

def validate_file_extension(file_extension):

    if file_extension not in ALLOWED_EXTENSIONS:
        raise ValueError("Invalid file format")

    return True
