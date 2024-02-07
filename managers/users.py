from fastapi.exceptions import HTTPException

from asyncpg import UniqueViolationError

from db import database
from managers.auth import AuthManager
from models import User


users = User.metadata.tables.get("users")


class UserManager:
    @staticmethod
    async def create_user(email: str, first_name: str, last_name: str):
        try:
            id_ = await database.execute(users.insert().values(
                email=email,
                first_name=first_name,
                last_name=last_name
            ))
        except UniqueViolationError:
            raise HTTPException(400, "User with this email already exists")
        user_do = await database.fetch_one(
            users.select().where(users.c.id == id_)
        )
        return AuthManager.encode_token(user_do)

    @staticmethod
    async def google_authorize(email):
        user_do = await UserManager.get_user_by_email(email)

        if not user_do:
            raise HTTPException(400, "User with this email does not exist")
        return AuthManager.encode_token(user_do)

    @staticmethod
    async def get_user_by_email(email: str):
        return await database.fetch_one(
            users.select().where(users.c.email == email)
        )

    @staticmethod
    async def get_user_by_id(id: int):
        return await database.fetch_one(
            users.select().where(users.c.id == id)
        )
