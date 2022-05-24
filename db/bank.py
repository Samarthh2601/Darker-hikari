from __future__ import annotations
import aiosqlite
from collections import namedtuple

class Bank:
    conn: aiosqlite.Connection
    cur: aiosqlite.Cursor

    async def setup(self) -> None:
        self.conn = await aiosqlite.connect('./dbs/bank.db')
        self.cur = await self.conn.cursor() 
        await self.cur.execute(''' CREATE TABLE IF NOT EXISTS mainbank(id INTEGER PRIMARY KEY NOT NULL, wallet INTEGER, bank INTEGER)''')
        await self.conn.commit()
        self.named_tuple = namedtuple("user", ["id", "wallet", "bank",])

    async def all_records(self):
        _data = await self.cur.execute("SELECT * FROM mainbank")
        return await _data.fetchall()


    async def read(self, user_id: int) -> namedtuple[...]:
        _data = await self.cur.execute("SELECT * FROM mainbank WHERE id = ?", (user_id,))
        data = await _data.fetchone()
        if not data:
            return None
        return self.named_tuple(data[0], data[1], data[2])
    
    async def create(self, user_id: int, *, wallet_amount: int=500, bank_amount: int=1000) -> namedtuple[...]:
        _check = await self.read(user_id)
        if _check:
            return self.named_tuple(_check[0], _check[1], _check[2])
        await self.cur.execute("INSERT INTO mainbank(id, wallet, bank) VALUES(?, ?, ?)", (user_id, wallet_amount, bank_amount))
        await self.conn.commit()
        return self.named_tuple(user_id, wallet_amount, bank_amount)
            
    async def update(self, user_id: int, *, wallet: int=None, bank: int=None) -> bool:
        if not wallet and bank:
            return False
        if wallet and not bank:
            await self.cur.execute("UPDATE mainbank SET wallet = ? WHERE id = ?", (wallet, user_id,))
            await self.conn.commit()
        elif bank and not wallet:
            await self.cur.execute("UPDATE mainbank SET bank = ? WHERE id = ?", (bank, user_id,))
            await self.conn.commit()
        elif bank and wallet:
            await self.cur.execute("UPDATE mainbank SET wallet = ?, bank = ? WHERE id = ?", (wallet, bank, user_id,))
            await self.conn.commit()
        return True
