from __future__ import annotations
import aiosqlite
from collections import namedtuple

class Experience:
    conn: aiosqlite.Connection
    cur: aiosqlite.Cursor

    async def setup(self) -> None:
        self.conn = await aiosqlite.connect("./dbs/experiences.db")
        self.cur = await self.conn.cursor()
        await self.cur.execute(''' CREATE TABLE IF NOT EXISTS exps(id INTEGER PRIMARY KEY NOT NULL, guild_id INTEGER, xp INTEGER, level INTEGER)''')
        await self.conn.commit()
        self.named_tuple = namedtuple("user", ["id", "guild_id", "xp", "level",])

    async def all_records(self):
        _data = await self.cur.execute("SELECT * FROM exps")
        return await _data.fetchall()

    async def read(self, user_id: int, guild_id: int) -> namedtuple[...]:
        u_data = await self.cur.execute('''
            SELECT * FROM exps WHERE id = ? AND guild_id = ?
            ''', (user_id, guild_id,))
        _user_data = await u_data.fetchone()

        if not _user_data: return None

        return self.named_tuple(_user_data[0], _user_data[1], _user_data[2], _user_data[3])

    async def create_acc(self, user_id: int, guild_id: int, starting_xp: int, starting_level: int) -> namedtuple[...]:
        _check = await self.read(user_id, guild_id)
        if _check:
            return self.named_tuple(_check[0], _check[1], _check[2], _check[3])
        await self.cur.execute('''INSERT INTO exps(id, guild_id, xp, level) VALUES(?, ?, ?, ?)''', (user_id, guild_id, starting_xp, starting_level,))
        await self.conn.commit()
        return self.named_tuple(user_id, guild_id, starting_xp, starting_level)
        
    async def update(self, user_id: int, guild_id: int, *, xp: int=None, level: int=None) -> bool:
        
        if xp and not level:
            await self.cur.execute("UPDATE exps SET xp = ? WHERE id = ? AND guild_id = ?", (xp, user_id, guild_id,))
            await self.conn.commit()
            return True
        if level and not xp:
            await self.cur.execute("UPDATE exps SET level = ? WHERE id = ? AND guild_id = ?", (level, user_id, guild_id))
            await self.conn.commit()
            return True
        if xp and level:
            await self.cur.execute("UPDATE exps SET xp = ? , level = ? WHERE id = ? AND guild_id = ?",(xp,level,user_id, guild_id))
            await self.conn.commit()
            return True
        return False