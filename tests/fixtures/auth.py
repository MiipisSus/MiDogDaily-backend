from pytest import fixture
from fastapi.testclient import TestClient


def login(client: TestClient, username, password):
    data = {
        'username': username,
        'password': password
    }
    
    res = client.post('/auth/login/', data=data)

    assert res.status_code == 200, 'Admin login failed'
    
    token = res.json().get('access_token')
    assert token is not None, 'Token generation failed'
    
    return token

@fixture(scope='function')
def token_header(client: TestClient):
    def _create_header(role: str = 'admin'):
        token = login(client, role, '12345')
        return {
            'Authorization': f'Bearer {token}'
        }
        
    return _create_header