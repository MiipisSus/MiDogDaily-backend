from fastapi.testclient import TestClient

from tests.fixtures.auth import *
from tests.fixtures.generals import *


class TestTaskGet:
    def test_list_tasks_success_admin(self, client: TestClient, token_header, create_task):
        task: Task = create_task(1)
        
        header = token_header()
        
        response = client.get('/tasks/?user_id=1', headers=header)

        assert response.status_code == 200
        assert response.json().get('items')[0].get('id') == task.id
        
    def test_list_tasks_success_user(self, client: TestClient, token_header, create_user, create_task):
        user: User = create_user()
        task: Task = create_task(user.id)
        
        header = token_header(user.username)
        
        response = client.get(f'/tasks/?user_id={user.id}', headers=header)
        
        assert response.status_code == 200
        assert response.json().get('items')[0].get('id') == task.id
    
    def test_list_tasks_fail_forbidden(self, client: TestClient, token_header, create_user, create_task):
        user_1: User = create_user()
        task: Task = create_task(user_1.id)
        user_2: User = create_user()
        
        header = token_header(user_2.username)
        
        response = client.get(f'/tasks/?user_id={user_1.id}', headers=header)
        
        assert response.status_code == 403
    
    def test_list_tasks_fail_no_auth(self, client: TestClient):
        response = client.get('/tasks/?user_id=1')
        
        assert response.status_code == 401
        assert response.json().get('detail') == 'Not authenticated'
        

class TestTaskPost:
    def test_post_task_success_user(self, client: TestClient, token_header, create_user):
        user: User = create_user()
        data = create_task_data([1, 2], True)
        
        header = token_header(user.username)
        
        response = client.post('/tasks/', json=data, headers=header)
        
        assert response.status_code == 201
        assert response.json().get('title') == data.get('title')
        assert response.json().get('tags')[0].get('id') == 1
        
    def test_post_task_fail_no_auth(self, client: TestClient):
        data = create_task_data([1, 2], True)
        
        response = client.post('/tasks/', json=data)
        
        assert response.status_code == 401
        assert response.json().get('detail') == 'Not authenticated'
        

class TestTaskPut:
    def test_put_task_success_user(self, client: TestClient, token_header, create_user, create_task):
        user: User = create_user()
        task: Task = create_task(user.id)
        data = create_task_data([2, 3], json_format=True)
        
        header = token_header(user.username)
        
        response = client.put(f'/tasks/{task.id}/', json=data, headers=header)
        
        assert response.status_code == 200
        assert response.json().get('title') == data.get('title')
        assert response.json().get('tags')[0].get('id') == 2
        
    def test_put_task_fail_no_auth(self, client: TestClient, create_task):
        task: Task = create_task(1)
        data = create_task_data([2, 3], json_format=True)
        
        response = client.put('/tasks/1/', json=data)
        
        assert response.status_code == 401
        assert response.json().get('detail') == 'Not authenticated'
        

class TestTaskDelete:
    def test_delete_success(self, client: TestClient, token_header, create_task):
        task: Task = create_task(1)
        
        header = token_header()
        
        response = client.delete(f'/tasks/{task.id}/', headers=header)
        
        assert response.status_code == 204