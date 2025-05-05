import aiofiles


async def read_file(file_path: str) -> str:
    async with aiofiles.open(file_path, mode='r', encoding='UTF-8') as f:
        contents = await f.read()
        return contents


async def write_to_file(file_path: str, content: str):
    async with aiofiles.open(file_path, mode="w", encoding='UTF-8') as f:
        await f.write(content)
