from datetime import datetime

from pydantic import BaseModel

from apps.schema import DBSchema


class CallSchema(DBSchema):
    duration: int
    call_type: str
    date: datetime
    mark: int
    call_text: str


class CallLevelSchema(BaseModel):
    level: int
