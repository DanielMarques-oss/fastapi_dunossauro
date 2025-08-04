from dataclasses import asdict

import pytest
from sqlalchemy import select

from fast_zero.models import User


@pytest.mark.asyncio
async def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username='alice', password='secret', email='teste@test'
        )
        session.add(new_user)
        await session.commit()

    user = await session.scalar(select(User).where(User.username == 'alice'))

    assert asdict(user) == {
        'id': 1,
        'username': 'alice',
        'password': 'secret',
        'email': 'teste@test',
        'created_at': time,
        'updated_at': time,
    }


@pytest.mark.asyncio
async def test_update_user(session, mock_db_time):
    with mock_db_time(model=User):
        new_user = User(
            username='alice', password='secret', email='teste@test'
        )
        session.add(new_user)
        await session.commit()
        user = await session.scalar(
            select(User).where(User.username == 'alice')
        )
        initial_updated_at = user.updated_at
        user.username = 'alice2'

        await session.commit()

        user = await session.scalar(
            select(User).where(User.username == 'alice2')
        )

    assert user.updated_at > initial_updated_at
    assert user.username == 'alice2'
