import re
import pandas as pd


EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w+$'
PHONE_REGEX = r'^\+?\d{10,15}$'


def validate_email(email: str) -> bool:
    return bool(
        re.match(
            EMAIL_REGEX,
            str(email)
        )
    )


def validate_phone(phone: str) -> bool:
    return bool(
        re.match(
            PHONE_REGEX,
            str(phone)
        )
    )


def validate_date_range(
    df: pd.DataFrame,
    column: str
):
    df[column] = pd.to_datetime(
        df[column],
        errors='coerce'
    )

    return df[df[column].notnull()]