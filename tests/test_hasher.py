"""Модуль для теста получения хэшей."""

import json
import os
import tempfile

import pytest

from repo_downloader.hasher import (
    calculate_sha256,
    file_sha256,
    write_hashes_to_file,
)

EXP_HASH = '315f5bdb76d078c43b8ac0064e4a0164612b1fce77c869345bfc94c75894edd3'


@pytest.mark.asyncio()
async def test_calculate_sha256_add_tasks():
    with tempfile.TemporaryDirectory() as temp_dir:
        file_paths = [
            os.path.join(temp_dir, 'file1.txt'),
            os.path.join(temp_dir, 'file2.txt'),
        ]
        for file_path in file_paths:
            with open(file_path, 'w') as file_handle:
                file_handle.write('Some content')

        sha256_hashes = await calculate_sha256(temp_dir)

        for file_path in file_paths:  # Noqa WPS440
            assert file_path in sha256_hashes


@pytest.mark.asyncio()
async def test_calculate_sha256_store_results():
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, 'test_file.txt')
        with open(file_path, 'w') as file_handle:
            file_handle.write('Hello, world!')

        sha256_hashes = await calculate_sha256(temp_dir)

        expected_hash = EXP_HASH
        assert sha256_hashes[file_path] == expected_hash


@pytest.mark.asyncio()
async def test_calculate_sha256_empty_folder():
    with tempfile.TemporaryDirectory() as temp_dir:
        sha256_hash = await calculate_sha256(temp_dir)
        assert not sha256_hash 


@pytest.mark.asyncio()
async def test_calculate_sha256_single_file():
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, 'test_file.txt')
        with open(file_path, 'w') as test_file:
            test_file.write('Hello, world!')

        expected_hash = EXP_HASH
        hash_value = await file_sha256(file_path)
        assert hash_value[1] == expected_hash


@pytest.mark.asyncio()
async def test_write_hashes_to_file():
    with tempfile.TemporaryDirectory() as temp_dir:
        output_file = os.path.join(temp_dir, 'hashes.json')
        sha256_hash = {
            'file1.txt': 'hash1',
            'file2.txt': 'hash2',
        }
        await write_hashes_to_file(sha256_hash, output_file)

        with open(output_file, 'r') as json_file:
            loaded_hash = json.load(json_file)
            assert loaded_hash == sha256_hash
