import aiohttp
import aiosqlite

class Player:
    def __init__(
            self,
            *,
            nickname: str,
            clan: str,
            trust: int,
            playtime_ms: int,
            social_discord: str,
            social_telegram: str,
            social_youtube: str,
            social_tiktok: str,
            bio: str,
            friends_count: int,
            streak: int,
            level: int,
            x: int,
            y: int,
            z: int,
            world: str,
            friends: str):
        self.nickname = nickname
        self.clan = clan
        self.trust = trust
        self.playtime_ms = playtime_ms
        self.social_discord = social_discord
        self.social_telegram = social_telegram
        self.social_youtube = social_youtube
        self.social_tiktok = social_tiktok
        self.bio = bio
        self.friends_count = friends_count
        self.streak = streak
        self.level = level
        self.x = x
        self.y = y
        self.z = z
        self.world = world
        self.friends = friends

async def init_db(db_path: str):
    async with aiosqlite.connect(db_path) as db:
        await db.execute('''
        CREATE TABLE IF NOT EXISTS players (
            username TEXT PRIMARY KEY,
            clan TEXT,
            trust INT,
            playtime_ms INT,
            social_discord TEXT,
            social_telegram TEXT,
            social_youtube TEXT,
            social_tiktok TEXT,
            bio TEXT,
            friends_count INT,
            streak INT,
            level INT,
            x INT,
            y INT,
            z INT,
            world TEXT,
            friends TEXT
        )
    ''')
        await db.commit()

async def write(db_path: str, player: Player):
    async with aiosqlite.connect(db_path) as db:
        await db.execute("INSERT OR REPLACE INTO players (username, clan, trust, playtime_ms, social_discord, social_telegram, social_youtube, social_tiktok, bio, friends_count, streak, level, x, y, z, world, friends) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", tuple(vars(player).values()))
        await db.commit()

async def read(db_path: str, nickname: str):
    async with aiosqlite.connect(db_path) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM players WHERE username = ?", (nickname,)) as cursor:
            row = await cursor.fetchone()
            if not row:
                return None

            return Player(
                nickname = row["username"],
                clan = row["clan"],
                trust = row["trust"],
                playtime_ms = row["playtime_ms"],
                social_discord = row["social_discord"],
                social_telegram = row["social_telegram"],
                social_youtube = row["social_youtube"],
                social_tiktok = row["social_tiktok"],
                bio = row["bio"],
                friends_count = row["friends_count"],
                streak = row["streak"],
                level = row["level"],
                x = row["x"],
                y = row["y"],
                z = row["z"],
                world = row["world"],
                friends = row["friends"]
            )

async def get_coords(nickname: str):
    async with aiohttp.ClientSession() as session:
        async with session.get('http://map.vo-xo.com/maps/world/live/players.json') as resp:
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

async def get_friends(nickname: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.vo-xo.com/users/{nickname}/friends') as resp:
            if resp.status == 200:
                data = await resp.json()

                friends = []

                for item in data['items']:
                    friends.append(item['username'])

                friends_list = ';'.join(friends)
                return friends_list

            else:
                return ''

async def get_data(nickname: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.vo-xo.com/users/{nickname}') as resp:
            if resp.status == 200:
                data = await resp.json()
            else:
                return None

    identity = data.get('identity')
    nickname = identity.get('username').lower()
    clan = (identity.get('clan') or {}).get('tag')
    trust = data.get('trust')
    playtime_ms = data.get('playtime').get('total_ms')
    level = data.get('xp').get('level')

    social_discord = data.get('socials').get('discord')
    social_telegram = data.get('socials').get('telegram')
    social_youtube = data.get('socials').get('youtube')
    social_tiktok = data.get('socials').get('tiktok')
    bio = data.get('bio')

    friends_count = data.get('friends_count')
    streak = data.get('streak')
    friends = await get_friends(nickname)

    coords = await get_coords(nickname)

    player = Player(
        nickname = str(nickname),
        clan = str(clan),
        trust = int(trust),
        playtime_ms = int(playtime_ms),
        social_discord = str(social_discord),
        social_telegram = str(social_telegram),
        social_youtube = str(social_youtube),
        social_tiktok = str(social_tiktok),
        bio = str(bio),
        friends_count = int(friends_count),
        streak = int(streak),
        level = int(level),
        x = coords['x'],
        y = coords['y'],
        z = coords['z'],
        world = coords['world'],
        friends = friends
    )

    return player
