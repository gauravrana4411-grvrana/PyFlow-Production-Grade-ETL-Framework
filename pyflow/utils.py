import logging
import time
import pandas as pd
import chardet

from logging.handlers import RotatingFileHandler
from collections import Counter, defaultdict, deque
from contextlib import contextmanager
from sqlalchemy import create_engine


# Logging setup
logger = logging.getLogger("PyFlow")
logger.setLevel(logging.DEBUG)

handler = RotatingFileHandler(
    'logs/pyflow.log',
    maxBytes=5 * 1024 * 1024,
    backupCount=5
)

formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'
)

handler.setFormatter(formatter)
logger.addHandler(handler)


# Timing decorator
def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start = time.time()

        result = func(*args, **kwargs)

        end = time.time()
        logger.info(
            f"{func.__name__} executed in {end - start:.2f} seconds"
        )

        return result

    return wrapper


# Encoding detector
def detect_encoding(file_path: str) -> str:
    with open(file_path, 'rb') as file:
        raw_data = file.read(100000)

    result = chardet.detect(raw_data)
    return result['encoding']


# CSV generator
def read_large_csv(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            yield line


# Database context manager
@contextmanager
def db_connection(connection_string: str):
    engine = create_engine(connection_string)
    connection = engine.connect()

    try:
        yield connection
        connection.commit()

    except Exception as e:
        connection.rollback()
        raise e

    finally:
        connection.close()


# Counter example
def top_pickup_locations(df: pd.DataFrame):
    counter = Counter(df['PULocationID'])
    return counter.most_common(10)


# defaultdict example
def average_fare_by_hour(df: pd.DataFrame):
    grouped = defaultdict(list)

    for _, row in df.iterrows():
        hour = pd.to_datetime(
            row['tpep_pickup_datetime']
        ).hour

        grouped[hour].append(
            row['fare_amount']
        )

    return {
        hour: sum(values) / len(values)
        for hour, values in grouped.items()
    }


# deque rolling buffer
buffer = deque(maxlen=1000)