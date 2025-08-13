from sqladmin.authentication import AuthenticationBackend
from fastapi import Request
from fastapi.responses import RedirectResponse
from fast_zero.security import verify_password
from fast_zero.models import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fast_zero.database import engine


class AdminAuth(AuthenticationBackend):
    """Autenticação para o SQLAdmin"""

    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        # Busca o usuário no banco
        async with AsyncSession(engine, expire_on_commit=False) as session:
            user = await session.scalar(
                select(User).where(User.username == username)
            )

            if user and verify_password(password, user.password):
                # Armazena o usuário na sessão
                request.session.update({"user_id": user.id})
                return True

        return False

    async def logout(self, request: Request) -> bool:
        # Remove o usuário da sessão
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        # Verifica se o usuário está autenticado
        user_id = request.session.get("user_id")
        if not user_id:
            return False

        # Verifica se o usuário ainda existe
        async with AsyncSession(engine, expire_on_commit=False) as session:
            user = await session.scalar(select(User).where(User.id == user_id))
            return user is not None
