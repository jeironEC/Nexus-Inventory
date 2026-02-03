import pytest
from rest_framework.test import APIClient
from django.test import Client


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def client():
    return Client()
