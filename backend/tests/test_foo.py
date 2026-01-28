import pytest


def test_true():
    assert True


def test_math():
    assert 1 + 2 == 3


@pytest.mark.django_db
def test_database():
    assert True
