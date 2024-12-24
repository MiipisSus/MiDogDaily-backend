from fastapi.testclient import TestClient

from tests.fixtures.auth import *
from tests.fixtures.generals import *

class TestTagGet:
    def test_list_tags_success_admin(self, client: TestClient, token_header):
        header = token_header()
        
        response = client.get('/tags/', headers=header)
        
        assert response.status_code == 200
        assert len(response.json().get('items')) == 3
        
    def test_list_tags_success_user(self, client: TestClient, token_header, create_user, create_tag):
        user: User = create_user()
        create_tag(user.id, False)
        
        header = token_header(user.username)
        
        response = client.get('/tags/', headers=header)
        
        assert response.status_code == 200
        assert any(item['is_public'] is False for item in response.json().get('items')) 
    
    def test_list_tags_fail_no_auth(self, client: TestClient):
        response = client.get('/tags/')
        
        assert response.status_code == 401
        
class TestTagPost:
    def test_post_tag_success_admin(self, client: TestClient, token_header):
        data = create_tag_data()
        header = token_header()
        
        response = client.post('/tags/', json=data, headers=header)
        
        assert response.status_code == 201
        assert response.json().get('name') == data.get('name')
        assert response.json().get('is_public') == True
        
    def test_post_tag_success_user(self, client: TestClient, token_header, create_user):
        user: User = create_user()
        data = create_tag_data()
        header = token_header(user.username)
        
        response = client.post('/tags/', json=data, headers=header)
        
        assert response.status_code == 201
        assert response.json().get('name') == data.get('name')
        assert response.json().get('is_public') == False
        
    def test_post_tag_fail_no_auth(self, client: TestClient):
        data = create_tag_data()
        
        response = client.post('/tags/', json=data)
        
        assert response.status_code == 401
        assert response.json().get('detail') == 'Not authenticated'
        

class TestTagPut:
    def test_put_tag_success_admin(self, client: TestClient, token_header, create_user, create_tag):
        user: User = create_user()
        tag: Tag = create_tag(user.id, False)
        data = tag.model_dump()
        data.update(name='update_tag')
        header = token_header()
        
        response = client.put(f'/tags/{tag.id}/', json=data, headers=header)
        
        assert response.status_code == 200
        assert response.json().get('name') == 'update_tag'
        
    def test_put_tag_success_user(self, client: TestClient, token_header, create_user, create_tag):
        user: User = create_user()
        tag: Tag = create_tag(user.id, False)
        data = tag.model_dump()
        data.update(name='update_tag')
        header = token_header(user.username)
        
        response = client.put(f'/tags/{tag.id}/', json=data, headers=header)
        
        assert response.status_code == 200
        assert response.json().get('name') == 'update_tag'
        
    def test_put_tag_fail_forbidden(self, client: TestClient, token_header, create_user, create_tag):
        user: User = create_user()
        tag: Tag = create_tag(1, True)
        data = tag.model_dump()
        data.update(name='update_tag')
        header = token_header(user.username)
        
        response = client.put(f'/tags/{tag.id}/', json=data, headers=header)
        
        assert response.status_code == 403
    
    def test_put_tag_fail_no_auth(self, client: TestClient):
        response = client.put('/tags/1/')
        
        assert response.status_code == 401
        assert response.json().get('detail') == 'Not authenticated'


class TestTagDelete:
    def test_delete_tag_success_admin(self, client: TestClient, token_header, create_user, create_tag):
        user: User = create_user()
        tag: Tag = create_tag(user.id, False)
        header = token_header()
        
        response = client.delete(f'/tags/{tag.id}/', headers=header)
        
        assert response.status_code == 204
    
    def test_delete_tag_success_user(self, client: TestClient, token_header, create_user, create_tag):
        user: User = create_user()
        tag: Tag = create_tag(user.id, False)
        header = token_header(user.username)
        
        response = client.delete(f'/tags/{tag.id}/', headers=header)
        
        assert response.status_code == 204
        
    def test_delete_tag_fail_no_auth(self, client: TestClient):
        response = client.delete('/tags/1/')
        
        assert response.status_code == 401