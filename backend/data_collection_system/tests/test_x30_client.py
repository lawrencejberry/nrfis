import pytest

from ..x30.x30_protocol import GET_DATA, DATA

pytestmark = [pytest.mark.asyncio, pytest.mark.usefixtures("x30_instrument")]


async def test_get_data(x30_client):
    response = await x30_client.execute(GET_DATA())
    assert response == bytes(88)


async def test_stream_data(x30_client):
    streamer = x30_client.stream()
    assert await streamer.__anext__() == DATA(bytes(88) + b"XXXXXXXX")
    assert await streamer.__anext__() == DATA(bytes(88) + b"XXXXXXXX")
    x30_client.streaming = False
