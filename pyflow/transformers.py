import pandas as pd
import numpy as np

from pyflow.validators import validate_email


class Transformer:

    @staticmethod
    def handle_missing_values(df: pd.DataFrame):
        for column in df.select_dtypes(include=np.number):
            df[column] = df[column].fillna(df[column].median())

        for column in df.select_dtypes(include='object'):
            df[column] = df[column].fillna('Unknown')

        return df

    @staticmethod
    def remove_duplicates(df: pd.DataFrame):
        required_cols = [
            'tpep_pickup_datetime',
            'pulocationid',
            'dolocationid'
        ]

        existing_cols = [c for c in required_cols if c in df.columns]

        return df.drop_duplicates(subset=existing_cols)

    @staticmethod
    def detect_outliers(df: pd.DataFrame, column: str):

        if column not in df.columns:
            return df

        q1 = df[column].quantile(0.25)
        q3 = df[column].quantile(0.75)

        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        return df[
            (df[column] >= lower) &
            (df[column] <= upper)
        ]

    @staticmethod
    def extract_datetime_features(df: pd.DataFrame, column: str):

        if column not in df.columns:
            return df

        df[column] = pd.to_datetime(df[column], errors='coerce')

        df['hour'] = df[column].dt.hour
        df['day_of_week'] = df[column].dt.day_name()
        df['is_weekend'] = df[column].dt.weekday >= 5

        return df

    @staticmethod
    def flatten_json(df: pd.DataFrame):
        return pd.json_normalize(
            df.to_dict(orient='records')
        )

    @staticmethod
    def filter_rush_hour(df: pd.DataFrame):

        if 'hour' not in df.columns or 'fare_amount' not in df.columns:
            return df

        return df.query(
            "(hour >= 7 and hour <= 10 or hour >= 16 and hour <= 19) "
            "and fare_amount > 20"
        )

    @staticmethod
    def validate_emails(df: pd.DataFrame, column: str):

        if column not in df.columns:
            return df

        return df[
            df[column].apply(validate_email)
        ]