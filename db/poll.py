from __future__ import annotations
import aiosqlite
from collections import namedtuple

class Poll:
    conn: aiosqlite.Connection
    cur: aiosqlite.Cursor

    async def setup(self) -> None:
        self.conn = await aiosqlite.connect("./dbs/polls.db")
        self.cur = await self.conn.cursor()
        await self.cur.execute('''CREATE TABLE IF NOT EXISTS polls(channel_id INTEGER PRIMARY KEY, message_id INTEGER, time TIMESTAMP)''')
        await self.conn.commit()
        self.named_tuple = namedtuple("message", ["channel_id", "message_id", "time"])

    async def all_records(self):
        _data = await self.cur.execute("SELECT * FROM polls")
        return await _data.fetchall()

    async def read(self, channel_id: int, message_id: int) -> namedtuple[...]:
        u_data = await self.cur.execute('''SELECT * FROM polls WHERE channel_id = ? AND message_id = ?''', (channel_id, message_id,))
        _user_data = await u_data.fetchone()
        if not _user_data: return None
        return self.named_tuple(_user_data[0], _user_data[1], _user_data[2],)

    async def create(self, channel_id: int, message_id: int, timestamp) -> namedtuple[...]:
        _check = await self.read(channel_id, message_id)
        if _check:
            return self.named_tuple(_check[0], _check[1], _check[2])
        await self.cur.execute('''INSERT INTO polls(channel_id, message_id, time) VALUES(?, ?, ?)''', (channel_id, message_id, timestamp,))
        await self.conn.commit()
        return self.named_tuple(channel_id, message_id, timestamp,)