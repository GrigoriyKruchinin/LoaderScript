"""Модуль для вычисления хешей SHA256 файлов в указанной папке."""

import asyncio
import hashlib
import json
import os
from typing import Dict


async def calculate_sha256(folder_path: str) -> Dict[str, str]:  # Noqa WPS210
    """
    Вычисляет хеши SHA256 для всех файлов в указанной папке.

    Args:
        folder_path: Путь к папке с файлами.

    Returns:
        Словарь, где ключи - это пути к файлам, а значения - их хеши SHA256.
    """
    sha256_hash = {}

    tasks = []
    for root, _, files in os.walk(folder_path):
        for single_file in files:
            file_path = os.path.join(root, single_file)
            tasks.append(file_sha256(file_path))

    hash_results = await asyncio.gather(*tasks)

    for path, hash_value in hash_results:
        sha256_hash[path] = hash_value

    return sha256_hash


async def file_sha256(file_path: str) -> tuple[str, str]:
    """
    Вычисляет хеш SHA256 для указанного файла.

    Args:
        file_path: Путь к файлу.

    Returns:
        Кортеж, содержащий путь к файлу и его хеш SHA256.
    """
    sha256 = hashlib.sha256()

    with open(file_path, 'rb') as file_handle:
        while True:
            chunk_size = 4096
            chunk = file_handle.read(chunk_size)
            if not chunk:
                break
            sha256.update(chunk)

    return file_path, sha256.hexdigest()


async def write_hashes_to_file(
    sha256_hash: Dict[str, str],
    output_file: str,
) -> None:
    """
    Записывает хеши в файл.

    Args:
        sha256_hash: Словарь с хешами SHA256 файлов.
        output_file: Путь к выходному файлу, куда будут записаны хеши.
    """
    with open(output_file, 'w') as file_handle:
        json.dump(sha256_hash, file_handle, indent=4)
