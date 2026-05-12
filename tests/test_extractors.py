from pyflow.extractors import CSVExtractor
def test_csv_extractor():
    extractor = CSVExtractor('sample.csv')
    assert extractor is not None