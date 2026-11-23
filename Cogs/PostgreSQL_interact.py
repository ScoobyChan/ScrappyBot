import json
import os
from typing import Any
import asyncpg
from discord.ext import commands


async def setup(bot: commands.Bot) -> None:
    if os.getenv("POSTGRES_HOST"):
        await bot.add_cog(PostgreSQL_interact(bot))


class PostgreSQL_interact(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self._pool: asyncpg.Pool | None = None

    async def cog_load(self) -> None:
        required = (
            "POSTGRES_HOST",
            "POSTGRES_USER",
            "POSTGRES_PASSWORD",
            "POSTGRES_DATABASE",
        )
        missing = [name for name in required if not os.getenv(name)]
        if missing:
            raise RuntimeError(
                "Missing PostgreSQL configuration: " + ", ".join(missing)
            )

        self._pool = await asyncpg.create_pool(
            host=os.environ["POSTGRES_HOST"],
            port=int(os.getenv("POSTGRES_PORT", "5432")),
            user=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"],
            database=os.environ["POSTGRES_DATABASE"],
            min_size=1,
            max_size=5,
        )

        try:
            async with self._pool.acquire() as connection:
                await connection.execute(
                    """
                    CREATE TABLE IF NOT EXISTS bot_settings (
                        setting_key VARCHAR(191) PRIMARY KEY,
                        setting_value TEXT NOT NULL,
                        updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
                    )
                    """
                )
        except Exception:
            await self._pool.close()
            self._pool = None
            raise

    async def cog_unload(self) -> None:
        if self._pool is not None:
            await self._pool.close()
            self._pool = None

    def _require_pool(self) -> asyncpg.Pool:
        if self._pool is None:
            raise RuntimeError("PostgreSQL connection pool is not available")
        return self._pool

    async def get_value(self, key: str, default: Any = None) -> Any:
        if not key or len(key) > 191:
            raise ValueError("Setting keys must contain between 1 and 191 characters")

        pool = self._require_pool()
        async with pool.acquire() as connection:
            value = await connection.fetchval(
                "SELECT setting_value FROM bot_settings WHERE setting_key = $1",
                key,
            )

        if value is None:
            return default
        return json.loads(value)

    async def set_value(self, key: str, value: Any) -> None:
        if not key or len(key) > 191:
            raise ValueError("Setting keys must contain between 1 and 191 characters")

        serialized = json.dumps(value, ensure_ascii=False)
        pool = self._require_pool()
        async with pool.acquire() as connection:
            await connection.execute(
                """
                INSERT INTO bot_settings (setting_key, setting_value)
                VALUES ($1, $2)
                ON CONFLICT (setting_key) DO UPDATE
                SET setting_value = EXCLUDED.setting_value,
                    updated_at = CURRENT_TIMESTAMP
                """,
                key,
                serialized,
            )

    async def delete_value(self, key: str) -> bool:
        if not key or len(key) > 191:
            raise ValueError("Setting keys must contain between 1 and 191 characters")

        pool = self._require_pool()
        async with pool.acquire() as connection:
            deleted_key = await connection.fetchval(
                "DELETE FROM bot_settings WHERE setting_key = $1 RETURNING setting_key",
                key,
            )
        return deleted_key is not None
