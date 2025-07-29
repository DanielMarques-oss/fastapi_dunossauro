from http import HTTPStatus

from jwt import decode

from fast_zero.security import SECRET_KEY, create_access_token


def test_jwt():
    data = {'test': 'test'}
    token = create_access_token(data)

    decoded = decode(token, SECRET_KEY, algorithms=['HS256'])

    assert decoded['test'] == data['test']
    assert 'exp' in decoded


def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer token-invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_jwt_without_email_via_token(client, user):
    response = client.put(
        f'/users/{user.id}',
        headers={
            'Authorization': f'Bearer {create_access_token({"test": "test"})}'
        },
        json={
            'username': 'bob',
            'email': 'aa@gmail.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_jwt_without_user_via_token(client, user):
    response = client.put(
        f'/users/{user.id}',
        headers={
            'Authorization': f'Bearer {
                create_access_token({"sub": "smoketest@gmail.com"})
            }'
        },
        json={
            'username': 'bob',
            'email': 'aa@gmail.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
