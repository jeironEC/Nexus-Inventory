import pytest
from http import HTTPStatus
from django.urls import reverse


@pytest.mark.django_db
def test_schema_endpoint(api_client):
    url = reverse("schema")
    response = api_client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_docs_endpoint(api_client):
    url = reverse("docs")
    response = api_client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_reverse_schema_url():
    url = reverse("schema")
    assert url == "/v1/schema/"


@pytest.mark.django_db
def test_reverse_docs_url():
    url = reverse("docs")
    assert url == "/v1/docs/"
