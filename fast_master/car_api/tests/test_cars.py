import pytest
from fastapi import status


class TestCreateCar:
    @pytest.mark.asyncio
    async def test_create_car_success(
        self,
        client,
        auth_headers,
        car_data,
    ):
        response = client.post(
            '/api/v1/cars/',
            json=car_data,
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data['model'] == car_data['model']
        assert data['factory_year'] == car_data['factory_year']
        assert data['model_year'] == car_data['model_year']
        assert data['color'] == car_data['color']
        assert data['plate'] == car_data['plate'].upper()
        assert data['fuel_type'] == car_data['fuel_type']
        assert data['transmission'] == car_data['transmission']
        assert float(data['price']) == car_data['price']
        assert 'id' in data
        assert 'brand' in data
        assert 'owner' in data

    @pytest.mark.asyncio
    async def test_create_car_duplicate_plate(
        self,
        client,
        auth_headers,
        car,
    ):
        car_data = {
            'model': 'Another Car',
            'factory_year': 2022,
            'model_year': 2023,
            'color': 'Blue',
            'plate': car.plate,
            'fuel_type': 'gasoline',
            'transmission': 'manual',
            'price': 100000.00,
            'brand_id': car.brand_id,
            'owner_id': car.owner_id,
        }

        response = client.post(
            '/api/v1/cars/',
            json=car_data,
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'Placa já está em uso' in response.json()['detail']

    @pytest.mark.asyncio
    async def test_create_car_invalid_brand(
        self,
        client,
        auth_headers,
        car_data,
        user,
    ):
        car_data['brand_id'] = 999

        response = client.post(
            '/api/v1/cars/',
            json=car_data,
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'Marca não encontrada' in response.json()['detail']

    @pytest.mark.asyncio
    async def test_create_car_invalid_owner(
        self,
        client,
        auth_headers,
        car_data,
        brand,
    ):
        car_data['owner_id'] = 999

        response = client.post(
            '/api/v1/cars/',
            json=car_data,
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'Proprietario não encontrado' in response.json()['detail']

    @pytest.mark.asyncio
    async def test_create_car_short_model(
        self,
        client,
        auth_headers,
        car_data,
    ):
        car_data['model'] = 'A'

        response = client.post(
            '/api/v1/cars/',
            json=car_data,
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert '2 caracteres' in response.json()['detail'][0]['msg']

    @pytest.mark.asyncio
    async def test_create_car_invalid_plate(
        self,
        client,
        auth_headers,
        car_data,
    ):
        car_data['plate'] = 'ABC'

        response = client.post(
            '/api/v1/cars/',
            json=car_data,
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert '7 e 10 caracteres' in response.json()['detail'][0]['msg']

    @pytest.mark.asyncio
    async def test_create_car_invalid_year(
        self,
        client,
        auth_headers,
        car_data,
    ):
        car_data['factory_year'] = 1800

        response = client.post(
            '/api/v1/cars/',
            json=car_data,
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert '1900 e 2030' in response.json()['detail'][0]['msg']

    @pytest.mark.asyncio
    async def test_create_car_invalid_price(
        self,
        client,
        auth_headers,
        car_data,
    ):
        car_data['price'] = -100

        response = client.post(
            '/api/v1/cars/',
            json=car_data,
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert 'maior do que zero' in response.json()['detail'][0]['msg']

    @pytest.mark.asyncio
    async def test_create_car_unauthorized(self, client, car_data):
        response = client.post('/api/v1/cars/', json=car_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestListCars:
    @pytest.mark.asyncio
    async def test_list_cars_success(self, client, auth_headers, car):
        response = client.get('/api/v1/cars/', headers=auth_headers)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert 'cars' in data
        assert 'offset' in data
        assert 'limit' in data
        assert len(data['cars']) == 1
        assert data['cars'][0]['model'] == car.model

    @pytest.mark.asyncio
    async def test_list_cars_empty(self, client, auth_headers):
        response = client.get('/api/v1/cars/', headers=auth_headers)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['cars'] == []

    @pytest.mark.asyncio
    async def test_list_cars_search_by_model(
        self,
        client,
        auth_headers,
        car,
    ):
        response = client.get(
            f'/api/v1/cars/?search={car.model}',
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data['cars']) == 1
        assert data['cars'][0]['model'] == car.model

    @pytest.mark.asyncio
    async def test_list_cars_search_by_color(
        self,
        client,
        auth_headers,
        car,
    ):
        response = client.get(
            f'/api/v1/cars/?search={car.color}',
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data['cars']) == 1

    @pytest.mark.asyncio
    async def test_list_cars_search_by_plate(
        self,
        client,
        auth_headers,
        car,
    ):
        response = client.get(
            f'/api/v1/cars/?search={car.plate}',
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data['cars']) == 1

    @pytest.mark.asyncio
    async def test_list_cars_filter_by_brand(
        self,
        client,
        auth_headers,
        car,
    ):
        response = client.get(
            f'/api/v1/cars/?brand_id={car.brand_id}',
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data['cars']) == 1

    @pytest.mark.asyncio
    async def test_list_cars_filter_by_fuel_type(
        self,
        client,
        auth_headers,
        car,
        car_data,
    ):
        fuel_type = car_data['fuel_type']
        response = client.get(
            f'/api/v1/cars/?fuel_type={fuel_type}',
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data['cars']) == 1

    @pytest.mark.asyncio
    async def test_list_cars_filter_by_transmission(
        self,
        client,
        auth_headers,
        car,
        car_data,
    ):
        transmission = car_data['transmission']
        response = client.get(
            f'/api/v1/cars/?transmission={transmission}',
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data['cars']) == 1

    @pytest.mark.asyncio
    async def test_list_cars_filter_by_availability(
        self,
        client,
        auth_headers,
        car,
    ):
        response = client.get(
            '/api/v1/cars/?is_available=true',
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data['cars']) == 1

    @pytest.mark.asyncio
    async def test_list_cars_filter_by_price_range(
        self,
        client,
        auth_headers,
        car,
    ):
        response = client.get(
            '/api/v1/cars/?min_price=100000&max_price=200000',
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data['cars']) == 1

    @pytest.mark.asyncio
    async def test_list_cars_with_pagination(
        self,
        client,
        auth_headers,
        car,
    ):
        response = client.get(
            '/api/v1/cars/?offset=0&limit=1',
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['offset'] == 0
        assert data['limit'] == 1

    @pytest.mark.asyncio
    async def test_list_cars_unauthorized(self, client):
        response = client.get('/api/v1/cars/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestGetCar:
    @pytest.mark.asyncio
    async def test_get_car_success(
        self,
        client,
        auth_headers,
        car,
    ):
        response = client.get(
            f'/api/v1/cars/{car.id}',
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['id'] == car.id
        assert data['model'] == car.model
        assert data['plate'] == car.plate
        assert 'brand' in data
        assert 'owner' in data

    @pytest.mark.asyncio
    async def test_get_car_not_found(self, client, auth_headers):
        response = client.get('/api/v1/cars/999', headers=auth_headers)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert 'Carro não encontrado' in response.json()['detail']

    @pytest.mark.asyncio
    async def test_get_car_not_owner(
        self,
        client,
        auth_headers,
        car,
        user,
    ):
        response = client.get(
            f'/api/v1/cars/{car.id}',
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.asyncio
    async def test_get_car_unauthorized(self, client, car):
        response = client.get(f'/api/v1/cars/{car.id}')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestUpdateCar:
    @pytest.mark.asyncio
    async def test_update_car_success(
        self,
        client,
        auth_headers,
        car,
    ):
        update_data = {
            'model': 'Corolla Updated',
            'color': 'Black',
            'price': 160000.00,
        }

        response = client.put(
            f'/api/v1/cars/{car.id}',
            json=update_data,
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['model'] == 'Corolla Updated'
        assert data['color'] == 'Black'
        assert float(data['price']) == 160000.00

    @pytest.mark.asyncio
    async def test_update_car_partial(
        self,
        client,
        auth_headers,
        car,
    ):
        update_data = {'model': 'Corolla XE'}

        response = client.put(
            f'/api/v1/cars/{car.id}',
            json=update_data,
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['model'] == 'Corolla XE'
        assert data['color'] == car.color

    @pytest.mark.asyncio
    async def test_update_car_not_found(self, client, auth_headers):
        update_data = {'model': 'Updated'}

        response = client.put(
            '/api/v1/cars/999',
            json=update_data,
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert 'Carro não encontrado' in response.json()['detail']

    @pytest.mark.asyncio
    async def test_update_car_duplicate_plate(
        self,
        client,
        auth_headers,
        car,
        another_car,
    ):
        update_data = {'plate': 'XYZ9876'}

        response = client.put(
            f'/api/v1/cars/{car.id}',
            json=update_data,
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'Placa já está em uso' in response.json()['detail']

    @pytest.mark.asyncio
    async def test_update_car_invalid_brand(
        self,
        client,
        auth_headers,
        car,
    ):
        update_data = {'brand_id': 999}

        response = client.put(
            f'/api/v1/cars/{car.id}',
            json=update_data,
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'Marca não encontrada' in response.json()['detail']

    @pytest.mark.asyncio
    async def test_update_car_unauthorized(self, client, car):
        update_data = {'model': 'Updated'}

        response = client.put(f'/api/v1/cars/{car.id}', json=update_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestDeleteCar:
    @pytest.mark.asyncio
    async def test_delete_car_success(
        self,
        client,
        auth_headers,
        car,
    ):
        response = client.delete(
            f'/api/v1/cars/{car.id}',
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        get_url = f'/api/v1/cars/{car.id}'
        get_response = client.get(get_url, headers=auth_headers)
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_delete_car_not_found(self, client, auth_headers):
        response = client.delete(
            '/api/v1/cars/999',
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert 'Carro não encontrado' in response.json()['detail']

    @pytest.mark.asyncio
    async def test_delete_car_unauthorized(self, client, car):
        response = client.delete(f'/api/v1/cars/{car.id}')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
