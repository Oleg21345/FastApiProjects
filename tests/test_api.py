
import pytest
from httpx import AsyncClient, ASGITransport

from main import app
from asgi_lifespan import LifespanManager

#Passed
@pytest.mark.asyncio
async def test_get_user():
    async with LifespanManager(app):
        async with AsyncClient(transport=ASGITransport(app=app),
                               base_url="http://test") as ac:
            response = await ac.get("/users")
            print(f"Ip address 127.0.0.1\nЧас обробки запиту становить {response.elapsed.total_seconds()}")
            print(response)
            print(response.json())
            assert response.status_code == 200
            assert isinstance(response.json(), list)
            if response.json():
                user = response.json()[0]
                assert "name" in user
                assert "age" in user
                assert "email" in user
                assert "password" in user

# #Passed
# @pytest.mark.asyncio
# async def test_register_user():
#     async with LifespanManager(app):
#         async with AsyncClient(transport=ASGITransport(app=app),
#                                base_url="http://test") as ac:
#             resp = await ac.post("/users", json={
#                 "name": "Oleg",
#                 "age": 52,
#                 "email": "danilaolegrogov@gmail.com",
#                 "password": "12345",
#                 "password_repeat": "12345"
#             })
#             print(resp)
#             assert resp.status_code == 200
#             data = resp.json()
#             assert isinstance(data, dict)
#
#
# #Passed
# @pytest.mark.asyncio
# async def test_change_user():
#     async with LifespanManager(app):
#         async with AsyncClient(transport=ASGITransport(app=app),
#                                base_url="http://test") as ac:
#             resp = await ac.put("/users/8", json={
#                 "name": "Oleg",
#                 "age": 52,
#                 "email": "danilaolegrogov@gmail.com",
#                 "password": "12345",
#                 "password_repeat": "12345"
#             })
#             print(f"Response message {resp}")
#             assert resp.status_code == 200
#             data = resp.json()
#             assert isinstance(data, bool)
#
# #Passed
# @pytest.mark.asyncio
# async def test_delete_user():
#     async with LifespanManager(app):
#         async with AsyncClient(transport=ASGITransport(app=app),
#                                base_url="http://test") as ac:
#             resp = await ac.delete("/users/16")
#             print(f"Response result {resp}")
#             assert resp.status_code == 200
#             data = resp.json()
#             assert isinstance(data, bool)
#
# #Passed
# @pytest.mark.asyncio
# async def test_user():
#     async with LifespanManager(app):
#         async with AsyncClient(transport=ASGITransport(app=app),
#                                base_url="http://test") as ac:
#             resp = await ac.get("/users/8")
#             print(f"Response result {resp}")
#             assert resp.status_code == 200
#             data = resp.json()
#             assert isinstance(data, dict)
