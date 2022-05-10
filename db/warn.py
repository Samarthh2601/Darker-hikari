from __future__ import annotations
import aiosqlite
from collections import namedtuple


class Warns:
    conn: aiosqlite.Connection
    cur: aiosqlite.Cursor

    async def setup(self) -> None:
        self.conn = await aiosqlite.connect("./dbs/warns.db")
        self.cur = await self.conn.cursor()
        await self.cur.execute('''CREATE TABLE IF NOT EXISTS warnings(id INTEGER PRIMARY KEY NOT NULL, guild_id INTEGER, warns INTEGER)''')
        await self.conn.commit()
        self.named_tuple = namedtuple("user", ["id", "guild_id", "warns"])
    
    async def all_records(self):
        _data = await self.cur.execute("SELECT * FROM warnings")
        return await _data.fetchall()

    async def read(self, user_id: int, guild_id: int) -> namedtuple[...]:
        u_data = await  self.cur.execute('''
            SELECT * FROM warnings WHERE id = ? AND guild_id = ?
            ''', (user_id, guild_id,))
        _user_data = await u_data.fetchone()

        if not _user_data: return None

        return self.named_tuple(_user_data[0], _user_data[1], _user_data[2],)
    
    async def create_acc(self, user_id: int, guild_id: int, warns: int) -> namedtuple[...]:
        _check = await self.read(user_id, guild_id)
        if _check:
            return self.named_tuple(_check[0], _check[1], _check[2])
        await self.cur.execute('''INSERT INTO warnings(id, guild_id, warns) VALUES(?, ?, ?)''', (user_id, guild_id, warns))
        await self.conn.commit()
        return self.named_tuple(user_id, guild_id, warns)
    

    async def update(self, user_id: int, guild_id: int, warns: int):
        await self.cur.execute("UPDATE warnings SET warns = ? WHERE id = ? AND guild_id = ?", (warns, user_id, guild_id))
        await self.conn.commit()
    