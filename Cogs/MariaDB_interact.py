import json
import os
from typing import Any

import asyncmy
from asyncmy.cursors import DictCursor
from discord.ext import commands


async def setup(bot: commands.Bot) -> None:
    if os.environ["MARIADB_HOST"]:
        await bot.add_cog(MariaDB_interact(bot))


class MariaDB_interact(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self._pool: Any = None

    async def cog_load(self) -> None:
        required = ("MARIADB_HOST", "MARIADB_USER", "MARIADB_PASSWORD", "MARIADB_DATABASE")
        missing = [name for name in required if not os.getenv(name)]
        if missing:
            raise RuntimeError(
                "Missing MariaDB configuration: " + ", ".join(missing)
            )

        self._pool = await asyncmy.create_pool(
            host=os.environ["MARIADB_HOST"],
            port=int(os.getenv("MARIADB_PORT", "3306")),
            user=os.environ["MARIADB_USER"],
            password=os.environ["MARIADB_PASSWORD"],
            db=os.environ["MARIADB_DATABASE"],
            charset="utf8mb4",
            autocommit=True,
            minsize=1,
            maxsize=5,
        )

        try:
            async with self._pool.acquire() as connection:
                async with connection.cursor() as cursor:
                    await cursor.execute(
                        """
                        CREATE TABLE IF NOT EXISTS bot_settings (
                            setting_key VARCHAR(191) NOT NULL PRIMARY KEY,
                            setting_value LONGTEXT NOT NULL,
                            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                                ON UPDATE CURRENT_TIMESTAMP
                        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                        """
                    )
        except Exception:
            self._pool.close()
            await self._pool.wait_closed()
            self._pool = None
            raise

    async def cog_unload(self) -> None:
        if self._pool is not None:
            self._pool.close()
            await self._pool.wait_closed()
            self._pool = None

    def _require_pool(self) -> Any:
        if self._pool is None:
            raise RuntimeError("MariaDB connection pool is not available")
        return self._pool

    async def get_value(self, key: str, default: Any = None) -> Any:
        if not key or len(key) > 191:
            raise ValueError("Setting keys must contain between 1 and 191 characters")

        pool = self._require_pool()
        async with pool.acquire() as connection:
            async with connection.cursor(cursor=DictCursor) as cursor:
                await cursor.execute(
                    "SELECT setting_value FROM bot_settings WHERE setting_key = %s",
                    (key,),
                )
                row = await cursor.fetchone()

        if row is None:
            return default
        return json.loads(row["setting_value"])

    async def set_value(self, key: str, value: Any) -> None:
        if not key or len(key) > 191:
            raise ValueError("Setting keys must contain between 1 and 191 characters")

        serialized = json.dumps(value, ensure_ascii=False)
        pool = self._require_pool()
        async with pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(
                    """
                    INSERT INTO bot_settings (setting_key, setting_value)
                    VALUES (%s, %s)
                    ON DUPLICATE KEY UPDATE setting_value = VALUES(setting_value)
                    """,
                    (key, serialized),
                )

    async def delete_value(self, key: str) -> bool:
        if not key or len(key) > 191:
            raise ValueError("Setting keys must contain between 1 and 191 characters")

        pool = self._require_pool()
        async with pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(
                    "DELETE FROM bot_settings WHERE setting_key = %s",
                    (key,),
                )
                return cursor.rowcount > 0
