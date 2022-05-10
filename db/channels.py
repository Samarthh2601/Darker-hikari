from __future__ import annotations
import aiosqlite
from collections import namedtuple

class Channels:
    cur: aiosqlite.Cursor
    conn: aiosqlite.Connection

    async def setup(self) -> None:
        self.conn = await aiosqlite.connect("./dbs/channels.db")
        self.cur = await self.conn.cursor()
        await self.cur.execute(''' CREATE TABLE IF NOT EXISTS channels(id INTEGER PRIMARY KEY NOT NULL, welcome INTEGER, leave INTEGER, log INTEGER, vent INTEGER)''')
        await self.conn.commit()
        self.named_tuple = namedtuple("guild", ["id", "welcome", "leave", "log", "vent",])
    
    async def all_records(self):
        _data = await self.cur.execute("SELECT * FROM channels")
        return await _data.fetchall()

    async def read(self, guild_id: int) -> namedtuple[...]:
        g_data = await self.cur.execute('''
            SELECT * FROM channels WHERE id = ?
            ''', (guild_id,))
        _guild_data = await g_data.fetchone()

        if not _guild_data:
            return None

        return self.named_tuple(_guild_data[0], _guild_data[1], _guild_data[2], _guild_data[3], _guild_data[4])

    async def create_acc(self, guild_id: int, welcome: int, leave: int, log: int, vent: int) -> namedtuple[...]:
        _check = await self.read(guild_id)
        if _check:
            return self.named_tuple(_check[0], _check[1], _check[2], _check[3])
        await self.cur.execute('''INSERT INTO channels(id, welcome, leave, log, vent) VALUES(?, ?, ?, ?, ?)''', (guild_id, welcome, leave, log, vent))
        await self.conn.commit()
        return self.named_tuple(guild_id, welcome, leave, log, vent)
        
    async def update(self, guild_id: int, *, welcome: int=None, leave: int=None, log: int=None, vent: int=None) -> bool:
        if welcome:
            await self.cur.execute("UPDATE channels SET welcome = ? WHERE id = ?", (welcome, guild_id,))
            await self.conn.commit()
            return True
        if leave:
            await self.cur.execute("UPDATE channels SET leave = ? WHERE id = ?", (leave, guild_id,))
            await self.conn.commit()
            return True
        if log:
            await self.cur.execute("UPDATE channels SET log = ? WHERE id = ?", (log, guild_id,))
            await self.conn.commit()
            return True
        if vent:
            await self.cur.execute("UPDATE channels SET vent = ? WHERE id = ?", (vent, guild_id,))
        return False