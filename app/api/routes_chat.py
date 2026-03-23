from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_chat_usecase, get_current_user_id
from app.core.errors import ExternalServiceError
from app.schemas.chat import ChatMessagePublic, ChatRequest, ChatResponse
from app.usecases.chat import ChatUseCase


router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(
    payload: ChatRequest,
    user_id: Annotated[int, Depends(get_current_user_id)],
    chat_usecase: Annotated[ChatUseCase, Depends(get_chat_usecase)],
) -> ChatResponse:
    try:
        answer = await chat_usecase.chat(
            user_id=user_id,
            prompt=payload.prompt,
            system=payload.system,
            max_history=payload.max_history,
            temperature=payload.temperature,
        )
        return ChatResponse(answer=answer)
    except ExternalServiceError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        ) from exc


@router.get("/history", response_model=list[ChatMessagePublic])
async def get_history(
    user_id: Annotated[int, Depends(get_current_user_id)],
    chat_usecase: Annotated[ChatUseCase, Depends(get_chat_usecase)],
) -> list[ChatMessagePublic]:
    messages = await chat_usecase.get_history(user_id=user_id)
    return [ChatMessagePublic.model_validate(item) for item in messages]


@router.delete("/history")
async def delete_history(
    user_id: Annotated[int, Depends(get_current_user_id)],
    chat_usecase: Annotated[ChatUseCase, Depends(get_chat_usecase)],
) -> dict[str, str]:
    await chat_usecase.clear_history(user_id=user_id)
    return {"status": "ok"}