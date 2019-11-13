import pytest

from ..protocol import GET_DATA


@pytest.mark.asyncio
async def test_get_data(client):
    response = await client.execute(GET_DATA())
    assert response == bytes(88)
