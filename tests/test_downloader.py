"""Модуль для теста загрузки контента."""

import os

import pytest
from aiohttp import ClientSession
from aioresponses import aioresponses

from repo_downloader import downloader

TYPE = 'type'
FILE_FORMAT = 'file'
NAME = 'name'
DOWNLOAD_URL = 'download_url'


@pytest.mark.asyncio()
async def test_fetch_json():
    with aioresponses() as mock_responses:
        mock_url = 'http://example.com'
        mock_response = [
            {
                TYPE: FILE_FORMAT,
                DOWNLOAD_URL: 'http://example.com/file',
                NAME: 'test_file.txt',
            },
        ]
        mock_responses.get(mock_url, payload=mock_response)

        async with ClientSession() as session:
            json_data = await downloader.fetch_json(session, mock_url)

    assert isinstance(json_data, list)
    assert len(json_data) == 1
    assert json_data[0][TYPE] == 'file'
    assert DOWNLOAD_URL in json_data[0]


@pytest.mark.asyncio()
async def test_download_file(tmpdir: str):
    mock_url = 'http://example.com/file'
    tmp_file = os.path.join(tmpdir, 'test_file.txt')

    with aioresponses() as mock_responses:
        mock_responses .get(mock_url, body=b'test file content')

        async with ClientSession() as session:
            await downloader.download_file(session, mock_url, tmp_file)

    assert os.path.isfile(tmp_file)


@pytest.mark.asyncio()
async def test_download_content(tmpdir: str):
    mock_url = 'http://example.com/repo'
    tmp_dir = os.path.join(tmpdir, 'test_repo')

    with aioresponses() as mock_responses:
        mock_responses.get(mock_url, payload=[
            {
                TYPE: FILE_FORMAT,
                DOWNLOAD_URL: 'http://example.com/file1',
                NAME: 'file1.txt',
            },
            {
                TYPE: 'dir',
                'url': 'http://example.com/subdir',
                NAME: 'subdir',
            },
        ])

        mock_responses.get('http://example.com/file1', body=b'Hello, world!')

        mock_responses.get('http://example.com/subdir', payload=[
            {
                TYPE: FILE_FORMAT,
                DOWNLOAD_URL: 'http://example.com/file2',
                NAME: 'file2.txt',
            },
        ])
        mock_responses.get(
            'http://example.com/file2',
            body=b'This is file 2 content',
        )

        async with ClientSession() as session:
            await downloader.download_content(session, mock_url, tmp_dir)

    assert os.path.isfile(os.path.join(tmp_dir, 'file1.txt'))
    assert os.path.isfile(os.path.join(tmp_dir, 'subdir', 'file2.txt'))
