from datetime import datetime, timedelta, timezone

import jwt
import pytest
from fastapi import status

from car_api.core.settings import Settings


class TestTokenGeneration:
    @pytest.mark.asyncio
    async def test_login_success(self, client, user, user_data):
        login_data = {
            'email': user_data['email'],
            'password': user_data['password'],
        }

        response = client.post('/api/v1/auth/token', json=login_data)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert 'access_token' in data
        assert data['token_type'] == 'bearer'
        assert len(data['access_token']) > 0

    @pytest.mark.asyncio
    async def test_login_invalid_email(self, client, user):
        login_data = {
            'email': 'nonexistent@example.com',
            'password': 'secret123',
        }

        response = client.post('/api/v1/auth/token', json=login_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert 'Incorrect email or password' in response.json()['detail']

    @pytest.mark.asyncio
    async def test_login_invalid_password(self, client, user, user_data):
        login_data = {
            'email': user_data['email'],
            'password': 'wrongpassword',
        }

        response = client.post('/api/v1/auth/token', json=login_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert 'Incorrect email or password' in response.json()['detail']

    @pytest.mark.asyncio
    async def test_login_invalid_email_format(self, client):
        login_data = {
            'email': 'invalid-email',
            'password': 'secret123',
        }

        response = client.post('/api/v1/auth/token', json=login_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    async def test_login_short_password(self, client, user_data):
        login_data = {
            'email': user_data['email'],
            'password': '12345',
        }

        response = client.post('/api/v1/auth/token', json=login_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert '6 caracteres' in response.json()['detail'][0]['msg']


class TestRefreshToken:
    @pytest.mark.asyncio
    async def test_refresh_token_success(self, client, auth_headers):
        response = client.post(
            '/api/v1/auth/refresh_token',
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert 'access_token' in data
        assert data['token_type'] == 'bearer'

    @pytest.mark.asyncio
    async def test_refresh_token_without_auth(self, client):
        response = client.post('/api/v1/auth/refresh_token')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.asyncio
    async def test_refresh_token_invalid_token(self, client):
        headers = {'Authorization': 'Bearer invalid_token_here'}

        response = client.post(
            '/api/v1/auth/refresh_token',
            headers=headers,
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert 'Could not validate credentials' in response.json()['detail']

    @pytest.mark.asyncio
    async def test_refresh_token_expired_token(self, client):
        expired_payload = {
            'sub': '1',
            'exp': datetime.now(timezone.utc) - timedelta(minutes=1),
        }

        settings = Settings()
        expired_token = jwt.encode(
            expired_payload,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )

        headers = {'Authorization': f'Bearer {expired_token}'}

        response = client.post(
            '/api/v1/auth/refresh_token',
            headers=headers,
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert 'Token has expired' in response.json()['detail']


class TestTokenValidation:
    @pytest.mark.asyncio
    async def test_token_contains_user_id(self, client, user, user_data):
        login_data = {
            'email': user_data['email'],
            'password': user_data['password'],
        }

        response = client.post('/api/v1/auth/token', json=login_data)
        token = response.json()['access_token']

        settings = Settings()
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )

        assert 'sub' in payload
        assert payload['sub'] == str(user.id)
        assert 'exp' in payload

    @pytest.mark.asyncio
    async def test_protected_endpoint_without_token(self, client):
        response = client.get('/api/v1/brands/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.asyncio
    async def test_protected_endpoint_with_valid_token(
        self,
        client,
        auth_headers,
    ):
        response = client.get('/api/v1/brands/', headers=auth_headers)

        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.asyncio
    async def test_protected_endpoint_with_invalid_token(self, client):
        headers = {'Authorization': 'Bearer invalid_token'}

        response = client.get('/api/v1/brands/', headers=headers)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
