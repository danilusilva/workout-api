from typing import Annotated

from pydantic import UUID4, Field
from workout_api.contrib.schemas import BaseSchema

class CategoriaIn(BaseSchema):
    nome: Annotated[str, Field(description='Nome da categoria', example='Scale', max_length=50)] # type: ignore

class CategoriaOut(CategoriaIn):
    id: Annotated[UUID4, Field(description='ID do atleta')] # type: ignore
    
