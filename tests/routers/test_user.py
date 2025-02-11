from fastapi.testclient import TestClient
from fastapi import UploadFile

from tests.fixtures.auth import *
from tests.fixtures.generals import *
from app.core.models import Role


class TestUserGet:
    def test_get_user_success(self, client: TestClient, token_header):
        header = token_header('admin')
        response = client.get('/users/1/', headers=header)
        
        assert response.status_code == 200
        assert response.json().get('username') == 'admin'
        
    def test_get_user_fail_no_auth(self, client: TestClient, token_header, create_user):
        response = client.get('/users/1/')
        
        assert response.status_code == 401
        assert response.json().get('detail') == 'Not authenticated'
        
    def test_list_users_success(self, client: TestClient, token_header):
        header = token_header('admin')
        response = client.get('/users/', headers=header)
        
        assert response.status_code == 200
        assert len(response.json().get('items')) == 1

    def test_list_users_fail_no_auth(self, client: TestClient):
        response = client.get('/users/')

        assert response.status_code == 401
        assert response.json().get('detail') == 'Not authenticated'
        
    def test_get_user_me_success(self, client: TestClient, token_header, create_user):
        user: User = create_user()
        header = token_header(user.username)
        
        response = client.get('/users/me/', headers=header)
        
        assert response.status_code == 200
        assert response.json().get('username') == user.username
        
    def test_get_user_me_fail_no_auth(self, client: TestClient):
        response = client.get('/users/me/')
        
        assert response.status_code == 401
        assert response.json().get('detail') == 'Not authenticated'

class TestUserPost:
    def test_post_user_success(self, client: TestClient, token_header):
        header = token_header('admin')
        data = create_user_data(Role.SUPERUSER)
        
        response = client.post('/users/', json=data, headers=header)
        
        assert response.status_code == 201
        assert response.json().get('username') == data.get('username')
        
    def test_post_user_fail_repeat_username(self, client: TestClient, token_header):
        header = token_header('admin')
        data = create_user_data(Role.SUPERUSER)
        data['username'] = 'admin'
        response = client.post('/users/', json=data, headers=header)
        
        assert response.status_code == 400
        assert response.json().get('detail') == '該帳號名稱已存在'
        
    def test_register_user_success(self, client: TestClient):
        data = create_user_data(Role.SUPERUSER)
        
        response = client.post('/users/register/', json=data)
        
        assert response.status_code == 201
        assert response.json().get('username') == data.get('username')
        assert response.json().get('role').get('id') == 3
        
    def test_upload_headshot_success(self, client: TestClient, token_header, create_user):
        user: User = create_user()
        header = token_header(user.username)
        
        with open('tests/files/headshot.png', 'rb') as f:
            data = {
                'file': ('test.png', f, 'image/png')
            }
        
            response = client.post('/users/headshot/me/', headers=header, files=data)
        
        assert response.status_code == 200


class TestUserPut:
    def test_put_user_success(self, client: TestClient, token_header, create_user):
        header = token_header('admin')
        user: User = create_user()
        data = user.model_dump()
        data.update(username='update_user')
        response = client.put(f'/users/{user.id}/', json=data, headers=header)
        
        assert response.status_code == 200
        assert response.json().get('username') == 'update_user'
        
    def test_put_user_fail_repeat_username(self, client: TestClient, token_header, create_user):
        header = token_header('admin')
        user: User = create_user()
        data = user.model_dump()
        data.update(username='admin')
        response = client.put(f'/users/{user.id}/', json=data, headers=header)
        
        assert response.status_code == 400
        assert response.json().get('detail') == '該帳號名稱已存在'
        
    def test_put_user_fail_not_found(self, client: TestClient, token_header):
        header = token_header('admin')
        data = create_user_data()
        response = client.put('/users/5/', json=data, headers=header)
        
        assert response.status_code == 404
        
    def test_put_user_me_success(self, client: TestClient, token_header, create_user):
        user: User = create_user()
        header = token_header(user.username)
        data = create_user_data()
        data.update(username='update_user')
        response = client.put('/users/me/', json=data, headers=header)
        
        assert response.status_code == 200
        assert response.json().get('username') == 'update_user'


class TestUserDelete:
    def test_delete_user_success(self, client: TestClient, token_header, create_user):
        header = token_header('admin')
        user: User = create_user()
        
        response = client.delete(f'/users/{user.id}/', headers=header)
        
        assert response.status_code == 204
    
    def test_delete_user_fail_not_found(self, client: TestClient, token_header):
        header = token_header('admin')
        response = client.delete(f'/users/5/', headers=header)
        
        assert response.status_code == 404