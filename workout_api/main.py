from fastapi import FastAPI, Request, status, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from workout_api.routers import api_router
from workout_api.responses.standard_responses import StandardResponseError

# Inicializa a aplicação FastAPI
app = FastAPI(title="Workout API")

# Inclui o api_router principal na sua aplicação FastAPI
app.include_router(api_router)

# --- Manipulador de Exceções Personalizado para HTTPException (400, 404, 409, 500) ---
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Manipula HTTPExceptions para retornar um formato de erro padronizado.
    """
    error_response = StandardResponseError.create(
        code=exc.status_code,
        message=exc.detail,
        details={} # Você pode adicionar mais detalhes aqui se a HTTPException tiver
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.model_dump(), # Converte o schema Pydantic para dict
    )

# --- Manipulador de Exceções Personalizado para Erros 422 (Validação de Schema) ---
@app.exception_handler(RequestValidationError)
@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Manipula erros de validação (422 Unprocessable Entity) para retornar um formato de erro padronizado.
    """
    error_details_list = []
    for error in exc.errors():
        field = ".".join(map(str, error["loc"][1:]))
        message = error["msg"]
        error_details_list.append({"field": field, "message": message})
    
    # A mensagem principal pode ser mais genérica, e os detalhes conterão a lista de erros
    error_response = StandardResponseError.create(
        code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        message="Erro(s) de validação na requisição.",
        details={"validation_errors": error_details_list}
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response.model_dump(),
    )

# --- Rota raiz para redirecionar para a documentação ---
@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    """
    Redireciona a requisição da raiz para a documentação da API (/docs).
    """
    return RedirectResponse(url="/docs")

