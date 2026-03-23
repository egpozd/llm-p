from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import UnauthorizedError
from app.core.security import decode_access_token
from app.db.session import AsyncSessionLocal
from app.repositories.chat_messages import ChatMessageRepository
from app.repositories.users import UserRepository
from app.services.openrouter_client import OpenRouterClient
from app.usecases.auth import AuthUseCase
from app.usecases.chat import ChatUseCase


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


def get_user_repository(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> UserRepository:
    return UserRepository(session)


def get_chat_message_repository(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> ChatMessageRepository:
    return ChatMessageRepository(session)


def get_openrouter_client() -> OpenRouterClient:
    return OpenRouterClient()


def get_auth_usecase(
    users: Annotated[UserRepository, Depends(get_user_repository)],
) -> AuthUseCase:
    return AuthUseCase(users)


def get_chat_usecase(
    chat_messages: Annotated[
        ChatMessageRepository,
        Depends(get_chat_message_repository),
    ],
    openrouter_client: Annotated[
        OpenRouterClient,
        Depends(get_openrouter_client),
    ],
) -> ChatUseCase:
    return ChatUseCase(
        chat_messages=chat_messages,
        openrouter_client=openrouter_client,
    )


def get_current_user_id(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> int:
    try:
        payload = decode_access_token(token)
        sub = payload.get("sub")
        if sub is None:
            raise UnauthorizedError("Token subject is missing")
        return int(sub)
    except (ValueError, TypeError, UnauthorizedError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc