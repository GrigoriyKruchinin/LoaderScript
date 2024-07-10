"""Модуль для теста точки входа в основной скрипт."""

import json
import os
import tempfile

import aiohttp
import pytest
from aioresponses import aioresponses

from main import main

EXP_HASH1 = '76130dd839bd6067e980cc0a564d51f64fc6c3e6a5dfca59debef4bd13eb7523'
EXP_HASH2 = '172dfeec7d6d76cfa88f0e3a5a4a82ec3bb9404c7f974904ecb66bbdd9f00f0f'


@pytest.mark.asyncio()
async def test_main():  # Noqa WPS210
    url = 'http://example.com/repo'
    with tempfile.TemporaryDirectory() as temp_dir:
        download_dir = os.path.join(temp_dir, 'downloaded_files')
        hashes_file = os.path.join(temp_dir, 'hashes.json')

        mock_repo_response = [
            {
                'type': 'file',
                'download_url': 'http://example.com/file1',
                'name': 'file1.txt',
            },
            {
                'type': 'file',
                'download_url': 'http://example.com/file2',
                'name': 'file2.txt',
            },
        ]

        mock1_content = b'Content of file1'
        mock2_content = b'Content of file2'

        expected_hashes = {
            os.path.join(download_dir, 'file1.txt'): EXP_HASH1,
            os.path.join(download_dir, 'file2.txt'): EXP_HASH2,
        }

        with aioresponses() as mock_responses:
            mock_responses.get(url, payload=mock_repo_response)
            mock_responses.get('http://example.com/file1', body=mock1_content)
            mock_responses.get('http://example.com/file2', body=mock2_content)

            async with aiohttp.ClientSession() as session:
                await main(url, download_dir, hashes_file)

        assert os.path.isfile(os.path.join(download_dir, 'file1.txt'))
        assert os.path.isfile(os.path.join(download_dir, 'file2.txt'))

        with open(hashes_file, 'r') as file_handle:
            hashes = json.load(file_handle)

        for file_path, hash_value in expected_hashes.items():
            assert hashes[file_path] == hash_value
