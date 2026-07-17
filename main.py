import aiohttp
import asyncio

class Player:
    def __init__(self,*, nickname: str, clan: str, trust: int, playtime_ms: int, social_discord: str, social_telegram: str, social_youtube: str, social_tiktok: str, bio: str,friends: int, streak: int, level: int, coords: dict):
        self.nickname = nickname
        self.clan = clan
        self.trust = trust
        self.playtime_ms = playtime_ms
        self.social_discord = social_discord
        self.social_telegram = social_telegram
        self.social_youtube = social_youtube
        self.social_tiktok = social_tiktok
        self.bio = bio
        self.friends = friends
        self.streak = streak
        self.coords = coords
        self.level = level



async def get_coords(nickname: str):
    async with aiohttp.ClientSession() as session:
        async with session.get('http://burmalda.vo-xo.com:8106/maps/world/live/players.json') as resp:
            if resp.status == 200:
                data = await resp.json()

                x = 0
                y = 0
                z = 0
                world = None

                for player in data.get('players'):
                    if player['name'].lower() == nickname.lower():
                        try:
                            x = int(player['position']['x'])
                            y = int(player['position']['y'])
                            z = int(player['position']['z'])
                            world = 'overworld' if bool(player['foreign']) else 'nether'

                        except Exception as e:
                            print(e)

    coords = {
        'x': x,
        'y': y,
        'z': z,
        'world': world
    }

    return coords


async def auto(nickname: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.vo-xo.com/users/{nickname}') as resp:
            if resp.status == 200:
                data = await resp.json()


                nickname = data.get('identity').get('username')
                clan = data.get('identity').get('clan').get('tag')
                trust = data.get('trust')
                playtime_ms = data.get('playtime').get('total_ms')
                level = data.get('xp').get('level')

                social_discord = data.get('socials').get('discord')
                social_telegram = data.get('socials').get('telegram')
                social_youtube = data.get('socials').get('youtube')
                social_tiktok = data.get('socials').get('tiktok')
                bio = data.get('bio')

                friends = data.get('friends_count')
                streak = data.get('streak')

                coords = await get_coords(nickname)

                player = Player(
                    nickname=str(nickname),
                    clan=str(clan),
                    trust=int(trust),
                    playtime_ms=int(playtime_ms),
                    social_discord=str(social_discord),
                    social_telegram=str(social_telegram),
                    social_youtube=str(social_youtube),
                    social_tiktok=str(social_tiktok),
                    bio=str(bio),
                    friends=int(friends),
                    streak=int(streak),
                    level=int(level),
                    coords=dict(coords)
                )

                return player

            else:
                return None





async def main():
    try:
        user = await auto(input('nickname: '))

        print(f'Nickname: {user.nickname}')
        print(f'Clan: {user.clan}')
        print(f'Trust: {user.trust}')
        print(f'Playtime Hours: {user.playtime_ms//1000//3600}')
        try:
            print(f"X: {user.coords['x']} Y: {user.coords['y']} Z: {user.coords['z']}")
            print(f'Dimension: {user.coords["world"]}')
        except Exception as e:
            print(e, 'Player is not on server')
    except Exception as e:
        print(e, 'Try again with another nickname')


if __name__ == '__main__':
    asyncio.run(main())
