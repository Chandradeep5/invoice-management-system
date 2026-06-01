
import pandas as pd


def process_csv_in_chunks(
    file_path,
    chunk_size=1000
):

    for chunk in pd.read_csv(
        file_path,
        chunksize=chunk_size
    ):

        yield chunk