import pandas as pd
import time

from sqlalchemy import create_engine
from pyflow.utils import logger


class DatabaseLoader:

    def __init__(self, connection_string: str):
        self.connection_string = connection_string

    def connect_with_retry(
        self,
        retries: int = 3,
        delay: int = 2
    ):
        for attempt in range(retries):
            try:
                engine = create_engine(self.connection_string)
                return engine

            except Exception as e:
                logger.error(
                    f"Database connection failed: {e}"
                )

                time.sleep(delay)
                delay *= 2

        raise Exception(
            "Could not connect to database"
        )

    def load(
        self,
        df: pd.DataFrame,
        table_name: str
    ):
        engine = self.connect_with_retry()

        df.to_sql(
            table_name,
            con=engine,
            if_exists='append',
            index=False,
            chunksize=1000,
            method='multi'
        )

        logger.info(
            f"Loaded data into {table_name}"
        )