import pytest
from http import HTTPStatus


@pytest.mark.django_db
def test_healthcheck_status(client):
    response = client.get("/v1/health/")
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_healthcheck_json(client):
    response = client.get("/v1/health/")
    assert response.json() == {"health": "ok"}
