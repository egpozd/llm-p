from app.repositories.chat_messages import ChatMessageRepository
from app.services.openrouter_client import OpenRouterClient


class ChatUseCase:
    def __init__(
        self,
        chat_messages: ChatMessageRepository,
        openrouter_client: OpenRouterClient,
    ) -> None:
        self.chat_messages = chat_messages
        self.openrouter_client = openrouter_client

    async def chat(
        self,
        user_id: int,
        prompt: str,
        system: str | None = None,
        max_history: int = 10,
        temperature: float = 0.7,
    ) -> str:
        history = await self.chat_messages.get_history(user_id=user_id)

        messages: list[dict[str, str]] = []

        if system:
            messages.append({"role": "system", "content": system})

        if max_history > 0:
            history_slice = history[-max_history:]
        else:
            history_slice = []

        for item in history_slice:
            messages.append(
                {
                    "role": item.role,
                    "content": item.content,
                }
            )

        messages.append({"role": "user", "content": prompt})

        answer = await self.openrouter_client.chat(
            messages=messages,
            temperature=temperature,
        )

        await self.chat_messages.create_message(
            user_id=user_id,
            role="user",
            content=prompt,
        )
        await self.chat_messages.create_message(
            user_id=user_id,
            role="assistant",
            content=answer,
        )

        return answer

    async def get_history(self, user_id: int):
        return await self.chat_messages.get_history(user_id=user_id)

    async def clear_history(self, user_id: int) -> None:
        await self.chat_messages.delete_history(user_id=user_id)