import aiohttp
import asyncio


class Player:
    class Coords:
        def __init__(self, *, nickname):
            self.nickname = nickname.lower()
            self.world = None
            self.x = None
            self.y = None
            self.z = None

        def _data2coord(self, data, world_name):
            if data is None:
                return False
            
            for player in data['players']:
                if player['name'].lower() == self.nickname and not bool(player['foreign']):
                    self.x = int(player['position']['x'])
                    self.y = int(player['position']['y'])
                    self.z = int(player['position']['z'])
                    self.world = world_name
                    return True

            return False



        async def update(self):
            async with aiohttp.ClientSession() as session:
                async with session.get('https://map.vo-xo.com/maps/world/live/players.json') as resp:
                    resp.raise_for_status()
                    data_over = await resp.json()
                    self._data2coord(data_over, 'over')

                async with session.get('https://map.vo-xo.com/maps/world_the_nether/live/players.json') as resp:
                    resp.raise_for_status()
                    data_nether = await resp.json()
                    self._data2coord(data_nether, 'nether')

                ''' Заглушка для энда
                async with session.get('https://map.vo-xo.com/maps/#/live/players.json') as resp:
                    resp.raise_for_status()
                    data_end = await resp.json()
                    self._data2coord(data_end, 'end')
                
                '''



    class Clan:
        def __init__(self, *, tag):
            self.tag = tag
            self.members = None
            self.name = None
            self.description = None
            self.icon = None
            self.color_hex = None
            self.minecraft_color_code = None
            self.level = None
            self.members_count = None
            self.members_limit = None
            self.open = None
            self.members_can_invite = None
            self.creator_username = None
            self.playtime_ms = None
            self.members = None

        async def update(self):
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://api.vo-xo.com/clans/{self.tag}') as resp:
                    resp.raise_for_status()
                    data = await resp.json()

            self.members = [ _['user']['username'].lower() for _ in data['members'] ]
            self.name = data['name']
            self.description = data['description']
            self.icon = data['icon']
            self.color_hex = data['color_hex']
            self.minecraft_color_code = data['minecraft_color_code']
            self.level = data['level']
            self.members_count = data['members_count']
            self.members_limit = data['members_limit']
            self.open = data['open']
            self.members_can_invite = data['members_can_invite']
            self.creator_username = data['creator_username'].lower()
            self.playtime_ms = data['total_playtime_ms']

    def __init__(self, *, nickname: str):
        self.nickname = nickname.lower()
        self.clan = None
        self.trust = None
        self.social_discord = None
        self.social_telegram = None
        self.social_youtube = None
        self.social_tiktok = None
        self.bio = None
        self.friends_count = None
        self.friends = None
        self.streak = None
        self.playtime_ms = None
        self.level = None
        self.coords = self.Coords(nickname=self.nickname)

    async def update(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.vo-xo.com/users/{self.nickname}') as resp:
                resp.raise_for_status()
                data = await resp.json()

        identity = data.get('identity')
        tag = (identity.get('clan') or {}).get('tag')

        if tag is not None:
            self.clan = self.Clan(tag = tag)
            await self.clan.update()

        self.trust = data.get('trust')
        self.playtime_ms = data.get('playtime').get('total_ms')
        self.level = data.get('xp').get('level')

        self.social_discord = data.get('socials').get('discord')
        self.social_telegram = data.get('socials').get('telegram')
        self.social_youtube = data.get('socials').get('youtube')
        self.social_tiktok = data.get('socials').get('tiktok')
        self.bio = data.get('bio')

        self.friends_count = data.get('friends_count')
        self.streak = data.get('streak')

        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.vo-xo.com/users/{self.nickname}/friends') as resp:
                resp.raise_for_status()
                data = await resp.json()

        self.friends = [ _['username'].lower() for _ in data['items'] ]
        await self.coords.update()

async def all_players():
    page = 0
    async with aiohttp.ClientSession() as session:
        while True:
            page += 1

            async with session.get(f'https://api.vo-xo.com/community/players?sort=level&order=desc&page={page}') as resp:
                resp.raise_for_status()
                data = await resp.json()

            if data['items'] is not None:
                players = [ _['user']['username'] for _ in data['items'] ]

    return players

