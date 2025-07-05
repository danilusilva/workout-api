from typing import Any, Optional, Union, List, TypeVar, Generic
from pydantic import BaseModel, Field

# Define um TypeVar para o tipo de dado que será retornado no campo 'data'
# Removido 'bound=BaseModel' para permitir que T seja qualquer tipo, incluindo listas de BaseModel
T = TypeVar('T') 

# --- Schema para o formato de Erro ---
class ErrorDetails(BaseModel):
    """Detalhes adicionais do erro."""
    # Você pode adicionar mais campos aqui se precisar de detalhes específicos
    # para diferentes tipos de erro (ex: campo_invalido, valor_recebido)
    # Por enquanto, vamos manter simples.
    pass

class StandardResponseError(BaseModel):
    """Schema para respostas de erro padronizadas."""
    success: bool = Field(False, description="Indica se a requisição foi bem-sucedida.")
    data: None = Field(None, description="Dados da resposta (será nulo em caso de erro).")
    error: dict = Field(..., description="Objeto contendo informações do erro.")

    @classmethod
    def create(cls, code: Union[str, int], message: str, details: Optional[Any] = None) -> "StandardResponseError":
        error_content = {
            "code": str(code),
            "message": message,
            "details": details if details is not None else {}
        }
        return cls(error=error_content) # type: ignore

# --- Schema para o formato de Sucesso (Agora Genérico) ---
# Ordem de herança: BaseModel primeiro, depois Generic[T]
class StandardResponseSuccess(BaseModel, Generic[T]): 
    """Schema para respostas de sucesso padronizadas."""
    success: bool = Field(True, description="Indica se a requisição foi bem-sucedida.")
    # O campo 'data' agora usa o TypeVar T
    data: Optional[T] = Field(..., description="Dados da resposta.")
    error: None = Field(None, description="Objeto de erro (será nulo em caso de sucesso).")

    @classmethod
    def create(cls, data: T) -> "StandardResponseSuccess[T]":
        return cls(data=data) # type: ignore

