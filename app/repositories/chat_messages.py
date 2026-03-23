from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import ChatMessage


class ChatMessageRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_message(
        self,
        user_id: int,
        role: str,
        content: str,
    ) -> ChatMessage:
        message = ChatMessage(
            user_id=user_id,
            role=role,
            content=content,
        )
        self.session.add(message)
        await self.session.commit()
        await self.session.refresh(message)
        return message

    async def get_history(
        self,
        user_id: int,
    ) -> list[ChatMessage]:
        stmt = (
            select(ChatMessage)
            .where(ChatMessage.user_id == user_id)
            .order_by(ChatMessage.id.asc())
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def delete_history(
        self,
        user_id: int,
    ) -> None:
        stmt = delete(ChatMessage).where(ChatMessage.user_id == user_id)
        await self.session.execute(stmt)
        await self.session.commit()