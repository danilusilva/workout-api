from uuid import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PGUUID

class BaseModel(DeclarativeBase):
    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), default=UUID, nullable=False)