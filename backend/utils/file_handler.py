
import pandas as pd
import json

def read_file(file_path, file_extension):

    if file_extension == ".csv":
        df = pd.read_csv(file_path)

    elif file_extension == ".xlsx":
        df = pd.read_excel(file_path)

    elif file_extension == ".json":
        with open(file_path, "r") as file:
            data = json.load(file)

        df = pd.DataFrame(data)

    else:
        raise ValueError("Unsupported file format")

    return df
