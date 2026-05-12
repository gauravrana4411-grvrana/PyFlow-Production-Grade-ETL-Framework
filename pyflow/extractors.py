import pandas as pd

from abc import ABC, abstractmethod
from pyflow.utils import detect_encoding


class BaseExtractor(ABC):

    @abstractmethod
    def extract(self):
        pass


class CSVExtractor(BaseExtractor):

    def __init__(
        self,
        file_path: str,
        chunk_size: int = 100000
    ):
        self.file_path = file_path
        self.chunk_size = chunk_size

    def extract(self):
        encoding = detect_encoding(self.file_path)

        return pd.read_csv(
            self.file_path,
            chunksize=self.chunk_size,
            encoding=encoding,
            on_bad_lines='skip'
        )


class JSONExtractor(BaseExtractor):

    def __init__(self, file_path: str):
        self.file_path = file_path

    def extract(self):
        return pd.read_json(self.file_path)


class ParquetExtractor(BaseExtractor):

    def __init__(self, file_path: str):
        self.file_path = file_path

    def extract(self):
        return pd.read_parquet(self.file_path)


class ExcelExtractor(BaseExtractor):

    def __init__(self, file_path: str):
        self.file_path = file_path

    def extract(self):
        excel_file = pd.ExcelFile(self.file_path)

        frames = []

        for sheet in excel_file.sheet_names:
            frames.append(
                pd.read_excel(
                    self.file_path,
                    sheet_name=sheet
                )
            )

        return pd.concat(
            frames,
            ignore_index=True
        )