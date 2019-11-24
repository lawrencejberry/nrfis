import pytest

from ..protocol import GET_DATA


@pytest.mark.asyncio
async def test_get_data(client):
    response = await client.execute(GET_DATA())
    assert response == bytes(88)


@pytest.mark.asyncio
async def test_stream_data(client):
    streamer = client.stream_data()
    assert await streamer.__anext__() == bytes(88) + b"XXXXXXXX"
    assert await streamer.__anext__() == bytes(88) + b"XXXXXXXX"
    client.streaming = False
    assert (await streamer.__anext__())[-8:] == b"ZZZZZZZZ"
