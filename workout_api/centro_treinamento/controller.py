from uuid import uuid4
from fastapi import APIRouter, Body, status, HTTPException
from pydantic import UUID4
from workout_api.atleta.models import AtletaModel # Importando o modelo de Atleta para a verificação de deleção
from workout_api.centro_treinamento.schemas import CentroTreinamentoIn, CentroTreinamentoOut
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.contrib.dependencies import DatabaseDependency
from sqlalchemy.future import select
from workout_api.responses.standard_responses import StandardResponseSuccess, StandardResponseError # Importando os schemas padronizados

router = APIRouter()

# Criando um novo centro de treinamento
@router.post(
    "/",
     summary="Criando um novo centro de treinamento",
     status_code=status.HTTP_201_CREATED,
     response_model=StandardResponseSuccess[CentroTreinamentoOut], # Definindo o modelo de resposta padronizado
)
async def post(
    db_session: DatabaseDependency,
    centro_treinamento_in: CentroTreinamentoIn = Body(...)
) -> StandardResponseSuccess[CentroTreinamentoOut]: # Definindo o tipo de retorno da função
    
    # Verificando se já existe um centro de treinamento com o mesmo nome
    centro_treinamento_existente = (await db_session.execute(
        select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_in.nome.strip())
    )).scalars().first()

    if centro_treinamento_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, # 409 Conflict é apropriado para recurso existente
            detail=f"Já existe um centro de treinamento com o nome '{centro_treinamento_in.nome.strip()}'."
        )

    # Criando o objeto CentroTreinamentoOut com um novo ID
    centro_treinamento_out = CentroTreinamentoOut(id=uuid4(), **centro_treinamento_in.model_dump())
    # Criando o modelo CentroTreinamentoModel para persistência no banco de dados
    centro_treinamento_model = CentroTreinamentoModel(**centro_treinamento_out.model_dump())

    # Adicionando o centro de treinamento ao banco de dados
    db_session.add(centro_treinamento_model)
    # Persistindo as mudanças
    await db_session.commit()
    # Atualizando o objeto do modelo para incluir dados gerados pelo banco (ex: pk_id)
    await db_session.refresh(centro_treinamento_model)

    # Retornando o centro de treinamento criado no formato de sucesso padronizado
    return StandardResponseSuccess.create(data=CentroTreinamentoOut.model_validate(centro_treinamento_model))

# Consultando todos os centros de treinamento
@router.get(
    "/",
     summary="Consultando todos os centros de treinamento",
     status_code=status.HTTP_200_OK,
    response_model=StandardResponseSuccess[list[CentroTreinamentoOut]], # Definindo o modelo de resposta padronizado para uma lista
)
async def query_all_centros_treinamento(db_session: DatabaseDependency,) -> StandardResponseSuccess[list[CentroTreinamentoOut]]: # Definindo o tipo de retorno da função
    # Consultando todos os centros de treinamento no banco de dados
    centros_treinamento_models: list[CentroTreinamentoModel] = (await db_session.execute(select(CentroTreinamentoModel))).scalars().all() # type: ignore

    # Mapeando modelos SQLAlchemy para schemas Pydantic e retornando no formato padronizado
    return StandardResponseSuccess.create(data=[CentroTreinamentoOut.model_validate(ct) for ct in centros_treinamento_models])

# Consultando um centro de treinamento pelo ID
@router.get(
    "/{id}",
     summary="Consultando um centro de treinamento pelo ID",
     status_code=status.HTTP_200_OK,
     response_model=StandardResponseSuccess[CentroTreinamentoOut], # Definindo o modelo de resposta padronizado
)
async def query_centro_treinamento_by_id(id: UUID4, db_session: DatabaseDependency,) -> StandardResponseSuccess[CentroTreinamentoOut]: # Definindo o tipo de retorno da função
    # Buscando o centro de treinamento pelo ID
    centro_treinamento_model: CentroTreinamentoOut = (
        await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))
    ).scalars().first() # type: ignore

    # Verificando se o centro de treinamento foi encontrado
    if not centro_treinamento_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Centro de treinamento não encontrado no identificador: {id}",
        )

    # Retornando o centro de treinamento encontrado no formato de sucesso padronizado
    return StandardResponseSuccess.create(data=CentroTreinamentoOut.model_validate(centro_treinamento_model))

# Deletando um centro de treinamento pelo ID
@router.delete(
    "/{id}",
     summary="Deletando um centro de treinamento pelo ID",
     status_code=status.HTTP_204_NO_CONTENT
)
async def delete_centro_treinamento(id: UUID4, db_session: DatabaseDependency,) -> None: # Definindo o tipo de retorno da função (None para 204)
    # Buscando o centro de treinamento pelo ID
    centro_treinamento: CentroTreinamentoModel = (
        await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))
    ).scalars().first() # type: ignore

    # Verificando se o centro de treinamento foi encontrado
    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Centro de treinamento não encontrado no identificador: {id}",
        )
    
    # Verificando se o centro de treinamento possui atletas vinculados
    atletas_vinculados = (await db_session.execute(
        select(AtletaModel).filter_by(centro_treinamento_id=centro_treinamento.pk_id)
    )).scalars().all()

    if atletas_vinculados:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Não é possível excluir o centro de treinamento '{centro_treinamento.nome}' pois {len(atletas_vinculados)} "
                f"atleta(s) estão atualmente vinculado(s) a ele."
            )
        )
    
    try:
        # Deletando o centro de treinamento do banco de dados
        await db_session.delete(centro_treinamento)
        # Persistindo as mudanças
        await db_session.commit()
    except Exception as e:
        # Em caso de qualquer outro erro inesperado durante a deleção
        print(f'Erro ao excluir o centro de treinamento: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro interno ao tentar deletar o centro de treinamento."
        )
