"""Точка входа в скрипт."""

import asyncio

import aiohttp

from repo_downloader.downloader import download_content
from repo_downloader.hasher import calculate_sha256, write_hashes_to_file

API_URL = (
    'https://gitea.radium.group/api/v1/repos/' +
    'radium/project-configuration/contents'
)
DOWNLOAD_DIR = 'project-configuration'
HASHES_FILE = 'project-configuration/hashes.json'


async def main() -> None:
    """Скрипт для загрузки репозитория и вычисления SHA256 хэшей файлов."""
    async with aiohttp.ClientSession() as session:
        await download_content(session, API_URL, DOWNLOAD_DIR)

    sha256_hash = await calculate_sha256(DOWNLOAD_DIR)
    await write_hashes_to_file(sha256_hash, HASHES_FILE)


if __name__ == '__main__':
    asyncio.run(main())
