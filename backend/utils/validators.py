
ALLOWED_EXTENSIONS = [".csv", ".xlsx", ".json"]

def validate_file_extension(file_extension):

    if file_extension not in ALLOWED_EXTENSIONS:
        raise ValueError("Invalid file format")

    return True

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


def validate_file_size(file):

    file.seek(0, 2)

    size = file.tell()

    file.seek(0)

    if size > MAX_FILE_SIZE:
        raise ValueError(
            "File size exceeds 5 MB limit"
        )

    return True
