import pytest

from menu import create_app
from menu.config import TestingConfig
from menu.main.routes import cart
from flask import url_for

@pytest.fixture
def client():
    app = create_app()
    app.config.from_object(TestingConfig)
    with app.test_client() as client:
        with app.app_context():
            pass
        yield client

def test_homepage(client):
    response = client.get("/kebabs/")
    assert response.status_code == 200

def test_other_pages(client):
    response = client.get("/burgers/")
    assert response.status_code == 200
    response = client.get("/snacks/")
    assert response.status_code == 200
    response = client.get("/salads/")
    assert response.status_code == 200
    response = client.get("/drinks/")
    assert response.status_code == 200
    response = client.get("/dessert/")
    assert response.status_code == 200
    
def test_cart(client):
    response = client.get("/cart/")
    assert response.status_code == 200
    assert b"Please add something from the menu!" in response.data
