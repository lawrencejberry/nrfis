import pytest

from ..x55.x55_protocol import GET_DATA, DATA


@pytest.mark.asyncio
async def test_get_data(client):
    response = await client.execute(GET_DATA())
    assert response == bytes(88)


@pytest.mark.asyncio
async def test_stream_data(client):
    streamer = client.stream()
    assert await streamer.__anext__() == DATA(bytes(88) + b"XXXXXXXX")
    assert await streamer.__anext__() == DATA(bytes(88) + b"XXXXXXXX")
    client.streaming = False
