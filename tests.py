import unittest
import json
from app import app
import pytest
import json
from app import app as flask_app

@pytest.fixture
def flask_test_app():
    flask_app.config.update({
        "TESTING": True,
    })
    yield flask_app

@pytest.fixture
def client(flask_test_app):
    return flask_test_app.test_client()

def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200

def test_hello_api(client):
    response = client.get('/api/hello')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    assert data['message'] == 'Hello, World!'

def test_status_api(client):
    response = client.get('/api/status')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'status' in data
    assert data['status'] == 'OK'
    assert 'service' in data
    assert data['service'] == 'Flask Demo App'

def test_info_api(client):
    response = client.get('/api/info')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'hostname' in data
    assert 'ip' in data
    assert 'platform' in data
    assert 'python_version' in data
    assert 'environment' in data
class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_hello_world(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<!DOCTYPE html>', response.data)  # Check for HTML content

    def test_status_endpoint(self):
        response = self.app.get('/api/status')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'OK')
        self.assertEqual(data['service'], 'Flask Demo App')

if __name__ == '__main__':
    unittest.main()
