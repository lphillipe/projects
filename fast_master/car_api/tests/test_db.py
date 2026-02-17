import pytest
from sqlalchemy import select

from car_api.models import User


@pytest.mark.asyncio
async def test_create_user(session):
    new_user = User(
        username='joao',
        password='secret',
        email='teste@test.com',
    )

    session.add(new_user)
    await session.commit()

    user = await session.scalar(
        select(User).where(User.email == 'teste@test.com')
    )

    new_user_data = {
        'id': user.id,
        'username': user.username,
        'password': user.password,
        'email': user.email,
    }

    assert new_user_data == {
        'id': 1,
        'username': 'joao',
        'password': 'secret',
        'email': 'teste@test.com',
    }


@pytest.mark.asyncio
async def test_query_user_by_id(session):
    new_user = User(
        username='maria',
        password='secret123',
        email='maria@test.com',
    )

    session.add(new_user)
    await session.commit()

    user = await session.get(User, 1)

    assert user is not None
    assert user.username == 'maria'
    assert user.email == 'maria@test.com'


@pytest.mark.asyncio
async def test_delete_user(session):
    new_user = User(
        username='pedro',
        password='secret',
        email='pedro@test.com',
    )

    session.add(new_user)
    await session.commit()

    await session.delete(new_user)
    await session.commit()

    user = await session.get(User, 1)
    assert user is None


@pytest.mark.asyncio
async def test_update_user(session):
    new_user = User(
        username='ana',
        password='secret',
        email='ana@test.com',
    )

    session.add(new_user)
    await session.commit()

    new_user.username = 'ana_updated'
    await session.commit()
    await session.refresh(new_user)

    assert new_user.username == 'ana_updated'
