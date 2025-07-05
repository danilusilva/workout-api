from typing_extensions import Annotated, Optional
from pydantic import Field, PositiveFloat
from workout_api.categorias.schemas import CategoriaIn
from workout_api.centro_treinamento.schemas import CentroTreinamentoAtleta
from workout_api.contrib.schemas import BaseSchema, OutMixin

class Atleta(BaseSchema):
    nome: Annotated[str, Field(description='Nome do atleta', example='João', max_length=50)] # type: ignore
    cpf: Annotated[str, Field(description='CPF do atleta', example='12345678901', max_length=11)] # type: ignore
    idade: Annotated[int, Field(description='Idade do atleta', example=25)] # type: ignore
    peso: Annotated[PositiveFloat, Field(description='Peso do atleta em kg', example=70.5)] # type: ignore
    altura: Annotated[PositiveFloat, Field(description='Altura do atleta em metros', example=1.70)] # type: ignore
    sexo: Annotated[str, Field(description='Sexo do atleta', example='M', max_length=1)] # type: ignore
    categoria: Annotated[CategoriaIn, Field(description='Categoria do atleta')] # type: ignore
    centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(description='Centro de treinamento do atleta')] # type: ignore

class AtletaIn(Atleta):
    pass
class AtletaOut(Atleta, OutMixin):
    pass

class AtletaUpdate(BaseSchema):
      idade: Annotated[Optional[int], Field(None, description='Idade do atleta', example=25)] # type: ignore
      peso: Annotated[Optional[PositiveFloat], Field(None, description='Peso do atleta em kg', example=70.5)] # type: ignore
      altura: Annotated[Optional[PositiveFloat], Field(None, description='Altura do atleta em metros', example=1.70)] # type: ignore
      categoria: Annotated[Optional[CategoriaIn], Field(None, description='Categoria do atleta')] # type: ignore
      centro_treinamento: Annotated[Optional[CentroTreinamentoAtleta], Field(None, description='Centro de treinamento do atleta')] # type: ignore