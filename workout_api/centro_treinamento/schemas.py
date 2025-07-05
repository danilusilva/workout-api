from pydantic import Field
from pydantic import UUID4
from typing_extensions import Annotated
from workout_api.contrib.schemas import BaseSchema

class CentroTreinamentoIn(BaseSchema):
    nome: Annotated[str, Field(description='Nome do centro de treinamento', example='CT Treinamento', max_length=50)]  # type: ignore
    endereco: Annotated[str, Field(description='Endereço do centro de treinamento', example='Rua das Flores, 123', max_length=60)]  # type: ignore
    proprietario: Annotated[str, Field(description='Nome do proprietário do centro de treinamento', example='João da Silva', max_length=30)]  # type: ignore

class CentroTreinamentoAtleta(BaseSchema):
    nome: Annotated[str, Field(description='Nome do centro de treinamento', example='CT Treinamento', max_length=50)]  # type: ignore

class CentroTreinamentoOut(CentroTreinamentoIn):
    id: Annotated[UUID4, Field(description='Identificador do centro de treinamento')] # type: ignore
