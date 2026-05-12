import pandas as pd

from pyflow.transformers import Transformer


def test_remove_duplicates():
    df = pd.DataFrame({
        'tpep_pickup_datetime': ['2024-01-01', '2024-01-01'],
        'PULocationID': [1, 1],
        'DOLocationID': [2, 2]
    })

    result = Transformer.remove_duplicates(df)

    assert len(result) == 1