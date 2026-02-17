import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from car_api.app import app
from car_api.core.database import get_session
from car_api.core.security import get_password_hash
from car_api.models import Base
from car_api.models.cars import Brand, Car
from car_api.models.users import User


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine(url='sqlite+aiosqlite:///:memory:')

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def user_data():
    return {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'secret123',
    }


@pytest_asyncio.fixture
async def user(session, user_data):
    hashed_password = get_password_hash(user_data['password'])
    db_user = User(
        username=user_data['username'],
        email=user_data['email'],
        password=hashed_password,
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


@pytest_asyncio.fixture
async def brand_data():
    return {
        'name': 'Toyota',
        'description': 'Japanese car manufacturer',
        'is_active': True,
    }


@pytest_asyncio.fixture
async def brand(session, brand_data):
    db_brand = Brand(
        name=brand_data['name'],
        description=brand_data['description'],
        is_active=brand_data['is_active'],
    )
    session.add(db_brand)
    await session.commit()
    await session.refresh(db_brand)
    return db_brand


@pytest_asyncio.fixture
async def car_data(brand, user):
    return {
        'model': 'Corolla',
        'factory_year': 2023,
        'model_year': 2024,
        'color': 'Silver',
        'plate': 'ABC1234',
        'fuel_type': 'hybrid',
        'transmission': 'automatic',
        'price': 150000.00,
        'description': 'Sedan comfortable and economical',
        'is_available': True,
        'brand_id': brand.id,
        'owner_id': user.id,
    }


@pytest_asyncio.fixture
async def car(session, car_data):
    db_car = Car(**car_data)
    session.add(db_car)
    await session.commit()
    await session.refresh(db_car)
    return db_car


@pytest_asyncio.fixture
async def auth_headers(client, user, user_data):
    login_response = client.post(
        '/api/v1/auth/token',
        json={
            'email': user_data['email'],
            'password': user_data['password'],
        },
    )
    token = login_response.json()['access_token']
    return {'Authorization': f'Bearer {token}'}


@pytest_asyncio.fixture
async def another_brand(session):
    db_brand = Brand(
        name='Honda',
        description='Japanese car manufacturer',
        is_active=True,
    )
    session.add(db_brand)
    await session.commit()
    await session.refresh(db_brand)
    return db_brand


@pytest_asyncio.fixture
async def another_user(session):
    hashed_password = get_password_hash('secret123')
    db_user = User(
        username='anotheruser',
        email='another@example.com',
        password=hashed_password,
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


@pytest_asyncio.fixture
async def another_car(session, brand, user):
    db_car = Car(
        model='Civic',
        factory_year=2022,
        model_year=2023,
        color='Blue',
        plate='XYZ9876',
        fuel_type='gasoline',
        transmission='manual',
        price=120000.00,
        brand_id=brand.id,
        owner_id=user.id,
    )
    session.add(db_car)
    await session.commit()
    await session.refresh(db_car)
    return db_car
