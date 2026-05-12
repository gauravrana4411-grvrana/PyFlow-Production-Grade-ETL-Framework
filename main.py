# from pyflow.config_parser import load_config
# from pyflow.extractors import CSVExtractor
# from pyflow.transformers import Transformer
# from pyflow.loaders import DatabaseLoader
from pyflow.utils import logger
from pyflow import CSVExtractor, Transformer, DatabaseLoader, load_config
import pandas as pd

config = load_config('config/config.yaml')

try:
    extractor = CSVExtractor(
        config['extract']['file_path'],
        config['extract']['chunk_size']
    )

    loader = DatabaseLoader(
        config['load']['connection_string']
    )

    for i, chunk in enumerate(extractor.extract()):

        # =========================
        # STEP 1: Normalize schema
        # =========================
        chunk.columns = chunk.columns.str.lower()

        # =========================
        # STEP 2: Clean missing values
        # =========================
        chunk = Transformer.handle_missing_values(chunk)

        # =========================
        # STEP 3: Safe datetime parsing
        # =========================
        chunk['tpep_pickup_datetime'] = pd.to_datetime(
            chunk['tpep_pickup_datetime'],
            errors='coerce'
        )
        chunk['tpep_dropoff_datetime'] = pd.to_datetime(
            chunk['tpep_dropoff_datetime'],
            errors='coerce'
        )

        chunk = chunk.dropna(subset=[
            'tpep_pickup_datetime',
            'tpep_dropoff_datetime'
        ])

        # =========================
        # STEP 4: Transformations
        # =========================
        chunk = Transformer.remove_duplicates(chunk)
        chunk = Transformer.detect_outliers(chunk, 'fare_amount')
        chunk = Transformer.extract_datetime_features(
            chunk,
            'tpep_pickup_datetime'
        )

        # =========================
        # STEP 5: Safety check
        # =========================
        if chunk.empty:
            logger.warning(f"Chunk {i} skipped (empty after processing)")
            continue

        # =========================
        # STEP 6: Load
        # =========================
        loader.load(
            chunk,
            config['load']['table_name']
        )

        logger.info(f"Chunk {i} loaded successfully")

    logger.info("ETL completed successfully")


except Exception as e:
    logger.error(f"ETL failed: {e}")