from pyflow.validators import validate_email

def test_validate_email():
    assert validate_email('test@gmail.com') is True