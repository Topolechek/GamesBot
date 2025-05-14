import asyncpg
from typing import Optional

async def create_pool(config) -> asyncpg.Pool:
    return await asyncpg.create_pool(
        dsn=config.postgres.dsn() if config.postgres else None,
        min_size=5,
        max_size=20,
    )

async def init_db(pool: asyncpg.Pool):
    async with pool.acquire() as connection:
        await connection.execute("""
            CREATE TABLE IF NOT EXISTS games (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                price DECIMAL NOT NULL,
                platform TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

async def save_game_price(pool: asyncpg.Pool, name: str, price: float, platform: str):
    async with pool.acquire() as connection:
        await connection.execute(
            """
            INSERT INTO games (name, price, platform)
            VALUES ($1, $2, $3)
            ON CONFLICT (name, platform) DO UPDATE
            SET price = EXCLUDED.price, updated_at = CURRENT_TIMESTAMP
            """,
            name, price, platform
        )

async def get_game_price(pool: asyncpg.Pool, name: str, platform: str) -> Optional[dict]:
    async with pool.acquire() as connection:
        row = await connection.fetchrow(
            "SELECT price, updated_at FROM games WHERE name = $1 AND platform = $2",
            name, platform
        )
        return dict(row) if row else None