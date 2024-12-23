from fastapi.testclient import TestClient

from tests.fixtures.auth import *
from tests.fixtures.generals import *
from app.core.models import Role


class TestUserGet:
    def test_list_users_success(self, client: TestClient, token_header):
        header = token_header('admin')
        response = client.get('/users/admin/', headers=header)
        
        assert response.status_code == 200
        assert response.json().get('items') == []

    def test_list_users_fail_no_auth(self, client: TestClient):
        response = client.get('/users/admin/')

        assert response.status_code == 401
        assert response.json().get('detail') == 'Not authenticated'

    def test_get_user_success(self, client: TestClient, token_header, create_user):
        user = create_user()
        # 該使用者的權限
        header = token_header('user')
        response = client.get(f'/users/{user.id}/', headers=header)
        
        assert response.status_code == 200
        assert response.json().get('username') == 'user'
    
    def test_get_user_success_within_admin_auth(self, client: TestClient, token_header, create_user):
        user = create_user()
        # 管理員的權限
        header = token_header('admin')
        response = client.get(f'/users/{user.id}/', headers=header)
        
        assert response.status_code == 200
        assert response.json().get('username') == 'admin'
        
    def test_get_user_fail_user_not_access(self, client: TestClient, token_header, create_user):
        user1 = create_user('user1')
        user2 = create_user('user2')
        
        header = token_header('user1')
        response = client.get(f'/users/{user2.id}/', headers=header)
        
        assert response.status_code == 403
        assert response.json().get('detail') == 'Forbidden'


class TestUserPost:
    def test_post_user_success(self, client: TestClient):
        data = create_user_data('user', Role.USER)
        response = client.post('/users/', json=data)

        assert response.status_code == 201
        assert response.json().get('username') == 'user'
        assert response.json().get('role').get('id') == Role.USER
        
    def test_post_user_fail_validate(self, client: TestClient):
        data = create_user_data('admin', Role.USER)
        response = client.post('/users/', json=data)
        
        assert response.status_code == 400
        assert response.json().get('detail') == '該帳號名稱已存在'
        
    def test_post_user_admin_success(self, client: TestClient, token_header):
        data = create_user_data('superuser', Role.SUPERUSER)
        header = token_header('admin')
        response = client.post('/users/admin/', json=data, headers=header)
        
        assert response.status_code == 201
        assert response.json().get('username') == 'superuser'
        assert response.json().get('role').get('id') == Role.SUPERUSER
        
    def test_post_user_admin_fail_no_auth(self, client: TestClient):
        data = create_user_data('superuser', Role.SUPERUSER)
        response = client.post('/users/admin/', json=data)
        
        assert response.status_code == 401
        assert response.json().get('detail') == 'Not authenticated'


class TestUserPut:
    def test_put_user_success(self, db: Session, client: TestClient, token_header, create_user):
        user = create_user()
        data = user.model_dump()
        data.update(username='update_user')
        header = token_header('user')
        response = client.put(f'/users/{user.id}', json=data, headers=header)
        
        assert response.status_code == 200
        assert response.json().get('username') == 'update_user'