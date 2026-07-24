import asyncio
from other import Player

async def main():
    Pl = Player(nickname=input('Write user nickname: ')
    await Pl.update()

    print(f'World: {Pl.coords.world}')
    print(f'X: {Pl.coords.x}')
    print(f'Y: {Pl.coords.y}')
    print(f'Z: {Pl.coords.z}')

    print(f'Clan: {Pl.clan.name}')
    print(f'Members: {", ".join(Pl.clan.members)}')
if __name__ == '__main__':
    asyncio.run(main())
