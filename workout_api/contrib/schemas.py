from typing import Annotated
from datetime import datetime
from pydantic import UUID4, BaseModel, Field


class BaseSchema(BaseModel):
    class Config:
        extra = "forbid"
        from_attributes = True

class OutMixin(BaseSchema):
    id: Annotated[UUID4, Field(description='ID do atleta')] # type: ignore
    created_at: Annotated[datetime, Field(description='Data de criação do atleta')] # type: ignore
