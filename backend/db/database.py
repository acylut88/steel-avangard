import aiosqlite
import asyncio

DB_PATH = "backend\\db\\avangard.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS players (
                user_id INTEGER PRIMARY KEY,
                user_name TEXT,
                scrap INTEGER DEFAULT 0,
                tools INTEGER DEFAULT 0,
                steel INTEGER DEFAULT 0,
                ac_gold INTEGER DEFAULT 0,
                lt_lvl INTEGER DEFAULT 1,
                st_lvl INTEGER DEFAULT 1,
                tt_lvl INTEGER DEFAULT 1,
                td_lvl INTEGER DEFAULT 1,
                lt_upg INTEGER DEFAULT 0,
                st_upg INTEGER DEFAULT 0,
                tt_upg INTEGER DEFAULT 0,
                td_upg INTEGER DEFAULT 0,
                last_action TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()
    print("✅ База данных 'Стальной Авангард' инициализирована!")

async def register_player(user_id: int, user_name: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO players (user_id, user_name) VALUES (?, ?)",
            (user_id, user_name)
        )
        await db.commit()
        print(f"✅ Игрок {user_name} (ID: {user_id}) зарегистрирован!")
                         
async def get_player(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM players WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            if row:
                print(f"✅ Данные игрока с ID {user_id} получены!")
                return dict(row)
            print(f"❌ Игрок с ID {user_id} не найден!")
            return None

async def add_resources(user_id, scrap: int = 0, tools: int = 0, steel: int = 0, ac_gold: int = 0):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            UPDATE players
            SET scrap = scrap + ?,
                tools = tools + ?,
                steel = steel + ?,
                ac_gold = ac_gold + ?,
                last_action = CURRENT_TIMESTAMP
                WHERE user_id = ?
        """, (scrap, tools, steel, ac_gold, user_id))
        print(f"✅ Ресурсы добавлены игроку с ID {user_id}!")
        await db.commit()
                         
if __name__ == "__main__":
    # инициализируем базу данных (раскомментировать при первом запуске)
    # asyncio.run(init_db())

    # зарегистрируем игрока для теста
    # asyncio.run(register_player(12345678900, "Игрок1"))
    
    # получим данные игрока для теста
    player = asyncio.run(get_player(12345678900))
    print(player['scrap'])

    # asyncio.run(add_resources(12345678900, scrap=100, tools=50, steel=20, ac_gold=10))
    print("Запчасти: ", asyncio.run(get_player(12345678900))['scrap'])
