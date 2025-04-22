from pydantic import BaseModel, ConfigDict


class IDSchema(BaseModel):
    id: int


class DBSchema(IDSchema):
    model_config = ConfigDict(from_attributes=True)
