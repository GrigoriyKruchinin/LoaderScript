"""Модуль для загрузки содержимого репозитория."""

import asyncio
import os
from typing import Any, Dict, List

import aiofiles
import aiohttp
from loguru import logger


async def fetch_json(
    session: aiohttp.ClientSession,
    url: str,
) -> List[Dict[str, Any]]:
    """
    Получает JSON-данные с указанного URL.

    :param session: сессия aiohttp для выполнения запроса.
    :param url: URL для получения JSON.
    :return: Список словарей с содержимым.
    """
    async with session.get(url) as response:
        return await response.json()


async def download_file(
    session: aiohttp.ClientSession,
    url: str,
    path: str,
) -> None:
    """
    Скачивает файл и сохраняет его в указанное местоположение.

    :param session: сессия aiohttp для выполнения запроса.
    :param url: URL для скачивания файла.
    :param path: локальный путь для сохранения файла.
    """
    async with session.get(url) as response:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        async with aiofiles.open(path, 'wb') as file_handler:
            await file_handler.write(await response.read())
        logger.bind(path=path).info(f'Скачан файл: {path}')  # Noqa WPS305


async def download_content(
    session: aiohttp.ClientSession,
    url: str,
    local_path: str,
) -> None:
    """
    Загружает содержимое репозитория, включая файлы и директории.

    :param session: сессия aiohttp для выполнения запроса.
    :param url: URL для получения содержимого репозитория.
    :param local_path: локальный путь для сохранения содержимого.
    """
    repo_content = await fetch_json(session, url)
    tasks = []
    for repo_item in repo_content:
        if repo_item['type'] == 'dir':
            tasks.append(
                download_content(
                    session,
                    repo_item['url'],
                    os.path.join(local_path, repo_item['name']),
                ),
            )
        else:
            tasks.append(
                download_file(
                    session,
                    repo_item['download_url'],
                    os.path.join(local_path, repo_item['name']),
                ),
            )
    await asyncio.gather(*tasks)
