import pytest
from fastapi import status


class TestCreateBrand:
    @pytest.mark.asyncio
    async def test_create_brand_success(
        self,
        client,
        auth_headers,
        brand_data,
    ):
        response = client.post(
            '/api/v1/brands/',
            json=brand_data,
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data['name'] == brand_data['name']
        assert data['description'] == brand_data['description']
        assert data['is_active'] == brand_data['is_active']
        assert 'id' in data
        assert 'created_at' in data
        assert 'update_at' in data

    @pytest.mark.asyncio
    async def test_create_brand_minimal_data(self, client, auth_headers):
        brand_data = {'name': 'Honda'}

        response = client.post(
            '/api/v1/brands/',
            json=brand_data,
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data['name'] == 'Honda'
        assert data['is_active'] is True

    @pytest.mark.asyncio
    async def test_create_brand_duplicate_name(
        self,
        client,
        auth_headers,
        brand,
    ):
        brand_data = {
            'name': brand.name,
            'description': 'Another description',
        }

        response = client.post(
            '/api/v1/brands/',
            json=brand_data,
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'Nome da marca já está em uso' in response.json()['detail']

    @pytest.mark.asyncio
    async def test_create_brand_short_name(self, client, auth_headers):
        brand_data = {'name': 'A'}

        response = client.post(
            '/api/v1/brands/',
            json=brand_data,
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert '2 caracteres' in response.json()['detail'][0]['msg']

    @pytest.mark.asyncio
    async def test_create_brand_unauthorized(self, client, brand_data):
        response = client.post('/api/v1/brands/', json=brand_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestListBrands:
    @pytest.mark.asyncio
    async def test_list_brands_success(self, client, auth_headers, brand):
        response = client.get('/api/v1/brands/', headers=auth_headers)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert 'brands' in data
        assert 'offset' in data
        assert 'limit' in data
        assert len(data['brands']) == 1
        assert data['brands'][0]['name'] == brand.name

    @pytest.mark.asyncio
    async def test_list_brands_empty(self, client, auth_headers):
        response = client.get('/api/v1/brands/', headers=auth_headers)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['brands'] == []

    @pytest.mark.asyncio
    async def test_list_brands_with_search(
        self,
        client,
        auth_headers,
        brand,
    ):
        response = client.get(
            f'/api/v1/brands/?search={brand.name}',
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data['brands']) == 1
        assert data['brands'][0]['name'] == brand.name

    @pytest.mark.asyncio
    async def test_list_brands_with_search_no_results(
        self,
        client,
        auth_headers,
        brand,
    ):
        response = client.get(
            '/api/v1/brands/?search=NonExistent',
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data['brands']) == 0

    @pytest.mark.asyncio
    async def test_list_brands_filter_by_active(
        self,
        client,
        auth_headers,
        brand,
    ):
        response = client.get(
            '/api/v1/brands/?is_active=true',
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data['brands']) == 1

    @pytest.mark.asyncio
    async def test_list_brands_filter_by_inactive(
        self,
        client,
        auth_headers,
        brand,
    ):
        response = client.get(
            '/api/v1/brands/?is_active=false',
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data['brands']) == 0

    @pytest.mark.asyncio
    async def test_list_brands_with_pagination(
        self,
        client,
        auth_headers,
        brand,
    ):
        response = client.get(
            '/api/v1/brands/?offset=0&limit=1',
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['offset'] == 0
        assert data['limit'] == 1

    @pytest.mark.asyncio
    async def test_list_brands_unauthorized(self, client):
        response = client.get('/api/v1/brands/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestGetBrand:
    @pytest.mark.asyncio
    async def test_get_brand_success(
        self,
        client,
        auth_headers,
        brand,
    ):
        response = client.get(
            f'/api/v1/brands/{brand.id}',
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['id'] == brand.id
        assert data['name'] == brand.name
        assert data['description'] == brand.description

    @pytest.mark.asyncio
    async def test_get_brand_not_found(self, client, auth_headers):
        response = client.get('/api/v1/brands/999', headers=auth_headers)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert 'Marca não encontrada' in response.json()['detail']

    @pytest.mark.asyncio
    async def test_get_brand_unauthorized(self, client, brand):
        response = client.get(f'/api/v1/brands/{brand.id}')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestUpdateBrand:
    @pytest.mark.asyncio
    async def test_update_brand_success(
        self,
        client,
        auth_headers,
        brand,
    ):
        update_data = {
            'name': 'Toyota Updated',
            'description': 'Updated description',
            'is_active': False,
        }

        response = client.put(
            f'/api/v1/brands/{brand.id}',
            json=update_data,
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['name'] == 'Toyota Updated'
        assert data['description'] == 'Updated description'
        assert data['is_active'] is False

    @pytest.mark.asyncio
    async def test_update_brand_partial(
        self,
        client,
        auth_headers,
        brand,
    ):
        update_data = {'name': 'Toyota Updated'}

        response = client.put(
            f'/api/v1/brands/{brand.id}',
            json=update_data,
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['name'] == 'Toyota Updated'
        assert data['description'] == brand.description

    @pytest.mark.asyncio
    async def test_update_brand_not_found(self, client, auth_headers):
        update_data = {'name': 'Updated Brand'}

        response = client.put(
            '/api/v1/brands/999',
            json=update_data,
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert 'Marca não encontrada' in response.json()['detail']

    @pytest.mark.asyncio
    async def test_update_brand_duplicate_name(
        self,
        client,
        auth_headers,
        brand,
        another_brand,
    ):
        update_data = {'name': 'Honda'}

        response = client.put(
            f'/api/v1/brands/{brand.id}',
            json=update_data,
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'Nome da marca já está em uso' in response.json()['detail']

    @pytest.mark.asyncio
    async def test_update_brand_unauthorized(self, client, brand):
        update_data = {'name': 'Updated'}

        response = client.put(f'/api/v1/brands/{brand.id}', json=update_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestDeleteBrand:
    @pytest.mark.asyncio
    async def test_delete_brand_success(
        self,
        client,
        auth_headers,
        brand,
    ):
        response = client.delete(
            f'/api/v1/brands/{brand.id}',
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        get_url = f'/api/v1/brands/{brand.id}'
        get_response = client.get(get_url, headers=auth_headers)
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_delete_brand_not_found(self, client, auth_headers):
        response = client.delete(
            '/api/v1/brands/999',
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert 'Marca não encontrada' in response.json()['detail']

    @pytest.mark.asyncio
    async def test_delete_brand_with_cars(
        self,
        client,
        auth_headers,
        brand,
        car,
    ):
        response = client.delete(
            f'/api/v1/brands/{brand.id}',
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        detail_msg = 'Não é possível deletar marca que possui carros'
        assert detail_msg in response.json()['detail']

    @pytest.mark.asyncio
    async def test_delete_brand_unauthorized(self, client, brand):
        response = client.delete(f'/api/v1/brands/{brand.id}')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
