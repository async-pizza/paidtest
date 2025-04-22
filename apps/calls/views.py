from fastapi import APIRouter, Depends
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

from apps.calls.models import Call
from apps.calls.schema import CallSchema, CallLevelSchema
from apps.calls.types import CallType
from apps.calls.utils import get_level
from apps.common.auth.decorators import auth_wrapper
from apps.common.database import get_session
from apps.users.models import User

router = APIRouter(prefix="/calls", tags=["Calls"])


@router.get("/", response_model=list[CallSchema])
async def get_calls(
    call_type: CallType | None = None,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(auth_wrapper),
) -> list[Call]:
    search = [Call.user_id == user.id]
    if call_type:
        search.append(Call.call_type == call_type.value)
    return await Call.all(session, and_(*search))


@router.get("/level/")
async def get_calls_level(
    session: AsyncSession = Depends(get_session),
    user: User = Depends(auth_wrapper),
) -> CallLevelSchema:
    total_score = await Call.get_total_score(session, user.id)
    return CallLevelSchema(level=get_level(total_score))
