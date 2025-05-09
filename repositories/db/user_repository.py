from persistent.db.Users import User
from infrastructure.sql.connect import sqlite_connection, create_all_tables
from sqlalchemy import insert, select

class UserRepository:
    def __init__(self) -> None:
        self._sessionmaker = sqlite_connection()
        create_all_tables()
        
    async def put_user(self, name:str, email:str, password:str) -> None:
        stmp = insert(User).values({"email":email, "name":name, "password":password}) 
        
        async with self._sessionmaker() as session:
            await session.execute(stmp)
            await session.commit()
            
    async def get_user(self, email:str, password:str) -> str|None:
        stmp = select(User.id).where(User.password == password, User.email == email).limit(1)
            
        async with self._sessionmaker() as session:
            resp = await session.execute(stmp)
            
        row = resp.fetchone()
        if row is None:
            return None
        else:
            return row[0]