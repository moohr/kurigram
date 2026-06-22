import pytest

from pyrogram import filters
from tests.filters import Client, Message

c = Client()


@pytest.mark.asyncio
async def test_guest_filter_no_guest_id():
    f = filters.guest
    m = Message(text="hello")
    assert not await f(c, m)


@pytest.mark.asyncio
async def test_guest_filter_with_guest_id():
    f = filters.guest
    m = Message(text="hello", guest_query_id="abc123")
    assert await f(c, m)


@pytest.mark.asyncio
async def test_guest_text_filter():
    f = filters.guest_text
    m = Message(text="hello", guest_query_id="abc123")
    assert await f(c, m)


@pytest.mark.asyncio
async def test_guest_text_filter_no_text():
    f = filters.guest_text
    m = Message(caption="hello", guest_query_id="abc123")
    assert not await f(c, m)


@pytest.mark.asyncio
async def test_guest_text_filter_no_guest_id():
    f = filters.guest_text
    m = Message(text="hello")
    assert not await f(c, m)


@pytest.mark.asyncio
async def test_guest_photo_filter():
    f = filters.guest_photo
    m = Message(guest_query_id="abc123")
    m.photo = [{}]
    assert await f(c, m)


@pytest.mark.asyncio
async def test_guest_photo_filter_no_photo():
    f = filters.guest_photo
    m = Message(guest_query_id="abc123")
    assert not await f(c, m)


@pytest.mark.asyncio
async def test_guest_document_filter():
    f = filters.guest_document
    m = Message(guest_query_id="abc123")
    m.document = {"file_id": "xyz"}
    assert await f(c, m)


@pytest.mark.asyncio
async def test_guest_document_filter_no_document():
    f = filters.guest_document
    m = Message(guest_query_id="abc123")
    assert not await f(c, m)


@pytest.mark.asyncio
async def test_guest_combo_and():
    f = filters.guest & filters.guest_text
    m = Message(text="hello", guest_query_id="abc123")
    assert await f(c, m)


@pytest.mark.asyncio
async def test_guest_combo_and_fail():
    f = filters.guest & filters.guest_text
    m = Message(text="hello")
    assert not await f(c, m)
