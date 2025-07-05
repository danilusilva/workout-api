from uuid import uuid4
from fastapi import APIRouter, Body, status, HTTPException
from pydantic import UUID4
from workout_api.atleta.models import AtletaModel 
from workout_api.categorias.schemas import CategoriaIn, CategoriaOut
from workout_api.categorias.models import CategoriaModel
from workout_api.contrib.dependencies import DatabaseDependency
from sqlalchemy.future import select
from workout_api.responses.standard_responses import StandardResponseSuccess, StandardResponseError 
router = APIRouter()

# Criando uma nova categoria
@router.post(
    "/",
     summary="Criando uma nova categoria",
     status_code=status.HTTP_201_CREATED,
     response_model=StandardResponseSuccess[CategoriaOut], # Definindo o modelo de resposta padronizado
)
async def post(
    db_session: DatabaseDependency,
    categoria_in: CategoriaIn = Body(...)
) -> StandardResponseSuccess[CategoriaOut]: # Definindo o tipo de retorno da função
    
    # Verificando se já existe uma categoria com o mesmo nome
    categoria_existente = (await db_session.execute(
        select(CategoriaModel).filter_by(nome=categoria_in.nome.strip())
    )).scalars().first()

    if categoria_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail=f"Já existe uma categoria com o nome '{categoria_in.nome.strip()}'."
        )
    
    # Criando o objeto CategoriaOut com um novo ID
    categoria_out = CategoriaOut(id=uuid4(), **categoria_in.model_dump())
    # Criando o modelo CategoriaModel para persistência no banco de dados
    categoria_model = CategoriaModel(**categoria_out.model_dump())

    # Adicionando a categoria ao banco de dados
    db_session.add(categoria_model)
    # Persistindo as mudanças
    await db_session.commit()
    # Atualizando o objeto do modelo para incluir dados gerados pelo banco (ex: pk_id)
    await db_session.refresh(categoria_model)

    # Retornando a categoria criada no formato de sucesso padronizado
    return StandardResponseSuccess.create(data=CategoriaOut.model_validate(categoria_model))


# Consultando todas as categorias
@router.get(
    "/",
     summary="Consultando todas as categorias",
     status_code=status.HTTP_200_OK,
    response_model=StandardResponseSuccess[list[CategoriaOut]], # Definindo o modelo de resposta padronizado para uma lista
)
async def query_all_categories(db_session: DatabaseDependency,) -> StandardResponseSuccess[list[CategoriaOut]]: # Definindo o tipo de retorno da função
    # Consultando todas as categorias no banco de dados
    categorias_models: list[CategoriaModel] = (await db_session.execute(select(CategoriaModel))).scalars().all() # type: ignore

    # Mapeando modelos SQLAlchemy para schemas Pydantic e retornando no formato padronizado
    return StandardResponseSuccess.create(data=[CategoriaOut.model_validate(categoria) for categoria in categorias_models])


# Consultando uma categoria pelo ID
@router.get(
    "/{id}",
     summary="Consultando uma categoria pelo ID",
     status_code=status.HTTP_200_OK,
     response_model=StandardResponseSuccess[CategoriaOut], # Definindo o modelo de resposta padronizado
)
async def query_category_by_id(id: UUID4, db_session: DatabaseDependency,) -> StandardResponseSuccess[CategoriaOut]: # Definindo o tipo de retorno da função
    # Buscando a categoria pelo ID
    categoria_model: CategoriaModel = (
        await db_session.execute(select(CategoriaModel).filter_by(id=id))
    ).scalars().first() # type: ignore

    # Verificando se a categoria foi encontrada
    if not categoria_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoria não encontrada: {id}",
        )

    # Retornando a categoria encontrada no formato de sucesso padronizado
    return StandardResponseSuccess.create(data=CategoriaOut.model_validate(categoria_model))


# Deletando uma categoria pelo ID
@router.delete(
    "/{id}",
     summary="Deletando uma categoria pelo ID",
     status_code=status.HTTP_204_NO_CONTENT
)
async def delete_category(id: UUID4, db_session: DatabaseDependency,) -> None: # Definindo o tipo de retorno da função (None para 204)
    # Buscando a categoria pelo ID
    categoria: CategoriaModel = ( 
        await db_session.execute(select(CategoriaModel).filter_by(id=id))
    ).scalars().first() # type: ignore

    # Verificando se a categoria foi encontrada
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoria não encontrada no identificador: {id}",
        )
    
    # Verificando atletas vinculados antes de deletar
    atletas_vinculados = (await db_session.execute(
        select(AtletaModel).filter_by(categoria_id=categoria.pk_id)
    )).scalars().all()

    if atletas_vinculados:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=(
                f"Não é possível excluir a categoria '{categoria.nome}' pois {len(atletas_vinculados)} "
                f"atleta(s) estão atualmente vinculado(s) a ela. Por favor, mova o(s) atleta(s) para "
                f"outra categoria antes de tentar excluir esta."
            )
        )
    
    try:
        # Deletando a categoria do banco de dados
        await db_session.delete(categoria)
        # Persistindo as mudanças
        await db_session.commit()
    except Exception as e:
        # Em caso de qualquer outro erro inesperado durante a deleção
        print(f'Erro ao excluir a categoria: {e}') # Para depuração no console do servidor
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro interno ao tentar deletar a categoria." # Mensagem genérica para o cliente
        )