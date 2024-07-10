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


async def main(
    url: str = API_URL,
    download_dir: str = DOWNLOAD_DIR,
    hashes_file: str = HASHES_FILE,
) -> None:
    """Скрипт для загрузки репозитория и вычисления SHA256 хэшей файлов."""
    async with aiohttp.ClientSession() as session:
        await download_content(session, url=url, local_path=download_dir)

    sha256_hash = await calculate_sha256(folder_path=download_dir)
    await write_hashes_to_file(sha256_hash, output_file=hashes_file)


if __name__ == '__main__':
    asyncio.run(main())
