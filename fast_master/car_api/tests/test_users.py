import pytest
from fastapi import status


class TestCreateUser:
    @pytest.mark.asyncio
    async def test_create_user_success(self, client, user_data):
        response = client.post('/api/v1/users/', json=user_data)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data['username'] == user_data['username']
        assert data['email'] == user_data['email']
        assert 'id' in data
        assert 'created_at' in data
        assert 'update_at' in data
        assert 'password' not in data

    @pytest.mark.asyncio
    async def test_create_user_duplicate_username(
        self,
        client,
        user,
        user_data,
    ):
        user_data['email'] = 'another@example.com'

        response = client.post('/api/v1/users/', json=user_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'Username já está em uso' in response.json()['detail']

    @pytest.mark.asyncio
    async def test_create_user_duplicate_email(
        self,
        client,
        user,
        user_data,
    ):
        user_data['username'] = 'anotheruser'

        response = client.post('/api/v1/users/', json=user_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'Email já está em uso' in response.json()['detail']

    @pytest.mark.asyncio
    async def test_create_user_invalid_email(self, client):
        user_data = {
            'username': 'testuser',
            'email': 'invalid-email',
            'password': 'secret123',
        }

        response = client.post('/api/v1/users/', json=user_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    async def test_create_user_short_username(self, client):
        user_data = {
            'username': 'ab',
            'email': 'test@example.com',
            'password': 'secret123',
        }

        response = client.post('/api/v1/users/', json=user_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert '3 caracteres' in response.json()['detail'][0]['msg']

    @pytest.mark.asyncio
    async def test_create_user_short_password(self, client):
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': '12345',
        }

        response = client.post('/api/v1/users/', json=user_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert '6 caracteres' in response.json()['detail'][0]['msg']


class TestListUsers:
    @pytest.mark.asyncio
    async def test_list_users_success(self, client, user):
        response = client.get('/api/v1/users/')

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert 'users' in data
        assert 'offset' in data
        assert 'limit' in data
        assert len(data['users']) == 1
        assert data['users'][0]['username'] == user.username

    @pytest.mark.asyncio
    async def test_list_users_empty(self, client):
        response = client.get('/api/v1/users/')

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['users'] == []
        assert data['offset'] == 0
        assert data['limit'] == 100

    @pytest.mark.asyncio
    async def test_list_users_with_search(self, client, user):
        response = client.get('/api/v1/users/?search=testuser')

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data['users']) == 1
        assert data['users'][0]['username'] == 'testuser'

    @pytest.mark.asyncio
    async def test_list_users_with_search_no_results(self, client, user):
        response = client.get('/api/v1/users/?search=nonexistent')

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data['users']) == 0

    @pytest.mark.asyncio
    async def test_list_users_with_pagination(self, client, user):
        response = client.get('/api/v1/users/?offset=0&limit=1')

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['offset'] == 0
        assert data['limit'] == 1

    @pytest.mark.asyncio
    async def test_list_users_search_by_email(self, client, user):
        response = client.get('/api/v1/users/?search=test@example.com')

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data['users']) == 1
        assert data['users'][0]['email'] == 'test@example.com'


class TestGetUser:
    @pytest.mark.asyncio
    async def test_get_user_success(self, client, user):
        response = client.get(f'/api/v1/users/{user.id}')

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['id'] == user.id
        assert data['username'] == user.username
        assert data['email'] == user.email

    @pytest.mark.asyncio
    async def test_get_user_not_found(self, client):
        response = client.get('/api/v1/users/999')

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert 'Usuário não encontrado' in response.json()['detail']


class TestUpdateUser:
    @pytest.mark.asyncio
    async def test_update_user_success(
        self,
        client,
        user,
        auth_headers,
    ):
        update_data = {
            'username': 'updateduser',
            'email': 'updated@example.com',
        }

        response = client.put(
            f'/api/v1/users/{user.id}',
            json=update_data,
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data['username'] == 'updateduser'
        assert data['email'] == 'updated@example.com'

    @pytest.mark.asyncio
    async def test_update_user_password(
        self,
        client,
        user,
        auth_headers,
        user_data,
    ):
        update_data = {'password': 'newpassword123'}

        response = client.put(
            f'/api/v1/users/{user.id}',
            json=update_data,
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_201_CREATED

        login_data = {
            'email': user_data['email'],
            'password': 'newpassword123',
        }
        login_response = client.post('/api/v1/auth/token', json=login_data)
        assert login_response.status_code == status.HTTP_200_OK

    @pytest.mark.asyncio
    async def test_update_user_not_found(self, client, auth_headers):
        update_data = {'username': 'updateduser'}

        response = client.put(
            '/api/v1/users/999',
            json=update_data,
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert 'Usuário não encontrado' in response.json()['detail']

    @pytest.mark.asyncio
    async def test_update_user_duplicate_username(
        self,
        client,
        user,
        auth_headers,
        another_user,
    ):
        update_data = {'username': 'anotheruser'}

        response = client.put(
            f'/api/v1/users/{user.id}',
            json=update_data,
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'Username já em uso' in response.json()['detail']

    @pytest.mark.asyncio
    async def test_update_user_unauthorized(self, client, user):
        update_data = {'username': 'updateduser'}

        response = client.put(f'/api/v1/users/{user.id}', json=update_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestDeleteUser:
    @pytest.mark.asyncio
    async def test_delete_user_success(
        self,
        client,
        user,
        auth_headers,
    ):
        response = client.delete(
            f'/api/v1/users/{user.id}',
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        get_response = client.get(f'/api/v1/users/{user.id}')
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_delete_user_not_found(self, client, auth_headers):
        response = client.delete(
            '/api/v1/users/999',
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert 'Usuário não encontrado' in response.json()['detail']

    @pytest.mark.asyncio
    async def test_delete_user_unauthorized(self, client, user):
        response = client.delete(f'/api/v1/users/{user.id}')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
