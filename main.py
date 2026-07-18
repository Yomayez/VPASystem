import asyncio
from other import get_data, write, init_db

db_path = 'base.db'

async def main(nick):
    player = await get_data(nick)
    await write(db_path, player)

if __name__ == '__main__':
    asyncio.run(init_db(db_path))
    asyncio.run(main(input('Enter user nickname').lower()))
