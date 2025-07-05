from datetime import datetime
from fastapi import HTTPException
from uuid import uuid4
from fastapi import APIRouter, Body, status
from pydantic import UUID4
from workout_api.atleta.models import AtletaModel
from workout_api.atleta.schemas import AtletaIn, AtletaOut, AtletaUpdate
from workout_api.categorias.models import CategoriaModel
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.contrib.dependencies import DatabaseDependency
from sqlalchemy.future import select
from workout_api.responses.standard_responses import StandardResponseSuccess, StandardResponseError 
import pytz
from typing import Union, List # Importando Union e List para aceitar um ou múltiplos atletas

router = APIRouter()

# Criando um novo atleta ou múltiplos atletas
@router.post(
    "/",
     summary="Criando um novo atleta ou múltiplos atletas",
     status_code=status.HTTP_201_CREATED,
     # A resposta pode ser um único AtletaOut ou uma lista de AtletaOut
     response_model=StandardResponseSuccess[Union[AtletaOut, List[AtletaOut]]] 
)
async def post(
    db_session: DatabaseDependency,
    # Aceita um único objeto AtletaIn ou uma lista de objetos AtletaIn
    atleta_data_input: Union[AtletaIn, List[AtletaIn]] = Body(...) 
):
    # Lista para armazenar os atletas criados com sucesso
    created_athletes_out = []
    
    # Normaliza a entrada para sempre ser uma lista para facilitar a iteração
    if not isinstance(atleta_data_input, list):
        atleta_data_input = [atleta_data_input]

    for atleta_in in atleta_data_input:
        # Verificando se já existe um atleta com o CPF duplicado
        atleta_existente = (await db_session.execute(
            select(AtletaModel).filter_by(cpf=atleta_in.cpf)
        )).scalars().first()

        if atleta_existente:
            # Levanta um erro se o CPF já existe, interrompendo o processamento do lote
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Já existe um atleta cadastrado com o CPF '{atleta_in.cpf}'. Não foi possível processar o lote."
            )

        # Verificando se a categoria existe
        categoria_nome = atleta_in.categoria.nome.strip()
        categoria = (await db_session.execute(
            select(CategoriaModel).filter_by(nome=categoria_nome))
        ).scalars().first()

        if not categoria:
            # Levanta um erro se a categoria não for encontrada
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"A categoria '{categoria_nome}' não foi encontrada para o atleta com CPF '{atleta_in.cpf}'. Não foi possível processar o lote."
            )

        # Verificando se o centro de treinamento existe
        centro_treinamento_nome = atleta_in.centro_treinamento.nome.strip()
        centro_treinamento = (await db_session.execute(
            select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_nome))
        ).scalars().first()

        if not centro_treinamento:
            # Levanta um erro se o centro de treinamento não for encontrado
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"O centro de treinamento '{centro_treinamento_nome}' não foi encontrado para o atleta com CPF '{atleta_in.cpf}'. Não foi possível processar o lote."
            )
        
        try:
            # Obtendo a hora atual em UTC para gravação no banco de dados
            hora_utc = datetime.utcnow()
            
            # Criando o objeto AtletaOut com um novo ID e a data de criação
            atleta_out = AtletaOut(
                id=uuid4(), 
                created_at= hora_utc,
                **atleta_in.model_dump()
            )
            # Criando o AtletaModel para persistência no banco de dados
            atleta_model = AtletaModel(**atleta_out.model_dump(exclude={'categoria', 'centro_treinamento'}))

            # Atribuindo os IDs das categorias e centros de treinamento
            atleta_model.categoria_id = categoria.pk_id
            atleta_model.centro_treinamento_id = centro_treinamento.pk_id

            # Adicionando o modelo do atleta à sessão do banco de dados
            db_session.add(atleta_model)
            
            # Adicionando o objeto de saída do atleta à lista de retorno
            created_athletes_out.append(atleta_out) 

        except Exception as e:
            # Captura erros inesperados durante a criação de um atleta no lote
            print(f"Erro ao criar atleta com CPF {atleta_in.cpf}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao criar o atleta com CPF '{atleta_in.cpf}'. Por favor, tente novamente. Detalhes: {e}"
            )
    
    # Commitando todos os atletas adicionados na sessão de uma vez (transação)
    await db_session.commit()
    
    # Refrescando os modelos para carregar os relacionamentos para o retorno completo
    final_athletes_out = []
    for atleta_out_item in created_athletes_out:
        atleta_model_from_db = (await db_session.execute(select(AtletaModel).filter_by(id=atleta_out_item.id))).scalars().first()
        if atleta_model_from_db:
            await db_session.refresh(atleta_model_from_db)
            final_athletes_out.append(AtletaOut.model_validate(atleta_model_from_db))


    # Retornando o schema de sucesso padronizado
    # Se a entrada original foi um único atleta, retorna um único atleta.
    # Se a entrada original foi uma lista, retorna a lista de atletas.
    if len(final_athletes_out) == 1 and not isinstance(Body(...), list): # Verifica o tipo original da entrada
        return StandardResponseSuccess.create(data=final_athletes_out[0])
    else:
        return StandardResponseSuccess.create(data=final_athletes_out)

# Listando todos os atletas
@router.get(
    "/",
     summary="Consultando todos os atletas",
     status_code=status.HTTP_200_OK,
    response_model=StandardResponseSuccess[list[AtletaOut]], 
)
async def query_all_athletes(db_session: DatabaseDependency,) -> StandardResponseSuccess[list[AtletaOut]]: 
    # Consultando todos os atletas no banco de dados
    atletas_models: list[AtletaModel] = (await db_session.execute(select(AtletaModel))).scalars().all() # type: ignore


    # Mapeando modelos SQLAlchemy para schemas Pydantic e retornando no formato padronizado
    return StandardResponseSuccess.create(data=[AtletaOut.model_validate(atleta) for atleta in atletas_models])


# Listando atletas pelo id
@router.get(
    "/{id}",
     summary="Consultando um atleta pelo ID",
     status_code=status.HTTP_200_OK,
     response_model=StandardResponseSuccess[AtletaOut],
)
async def query_athlete_by_id(id: UUID4, db_session: DatabaseDependency,) -> StandardResponseSuccess[AtletaOut]:
    # Buscando o atleta pelo ID
    atleta_model: AtletaModel = ( 
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first() # type: ignore


    # Verificando se o atleta foi encontrado
    if not atleta_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Atleta não encontrado no identificador: {id}",
        )
    # Mapeando modelo SQLAlchemy para schema Pydantic e retornando no formato padronizado
    return StandardResponseSuccess.create(data=AtletaOut.model_validate(atleta_model))

# Atualizando informações do atleta pelo id
@router.patch(
    "/{id}",
     summary="Atualizando informações de um atleta pelo ID",
     status_code=status.HTTP_200_OK,
     response_model=StandardResponseSuccess[AtletaOut],
)
async def patch_athlete(id: UUID4, db_session: DatabaseDependency, atleta_up: AtletaUpdate = Body(...)) -> StandardResponseSuccess[AtletaOut]:
    # Buscando o atleta pelo ID
    atleta: AtletaModel = ( 
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()  

    # Verificando se o atleta foi encontrado
    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Atleta não encontrado no identificador: {id}",
        )
    
    atleta_update_data = atleta_up.model_dump(exclude_unset=True)

    for key, value in atleta_update_data.items():
        if key == "categoria" and value:
            categoria_nome = value.get("nome")
            if categoria_nome:
                categoria = (await db_session.execute(
                    select(CategoriaModel).filter_by(nome=categoria_nome))
                ).scalars().first()
                if not categoria:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"A categoria '{categoria_nome}' não foi encontrada para atualização."
                    )
                atleta.categoria = categoria
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Nome da categoria não fornecido para atualização."
                )

        elif key == "centro_treinamento" and value:
            ct_nome = value.get("nome")
            if ct_nome:
                centro_treinamento = (await db_session.execute(
                    select(CentroTreinamentoModel).filter_by(nome=ct_nome))
                ).scalars().first()
                if not centro_treinamento:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"O centro de treinamento '{ct_nome}' não foi encontrado para atualização."
                    )
                atleta.centro_treinamento = centro_treinamento
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Nome do centro de treinamento não fornecido para atualização."
                )
        else:
            setattr(atleta, key, value)

    await db_session.commit()
    await db_session.refresh(atleta)

    # Retornando a instância atualizada mapeada para o schema de saída no formato padronizado
    return StandardResponseSuccess.create(data=AtletaOut.model_validate(atleta))

# Deletando atleta pelo id
@router.delete(
    "/{id}",
     summary="Deletando um atleta pelo ID",
     status_code=status.HTTP_204_NO_CONTENT,
     response_model=None # Para 204 No Content, o corpo é vazio.
)
async def delete_athlete(id: UUID4, db_session: DatabaseDependency,) -> None:
    # Buscando o atleta pelo ID
    atleta: AtletaModel = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first() # type: ignore

    # Verificando se o atleta foi encontrado
    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Atleta não encontrado no identificador: {id}",
        )
    
    try:
        # Deletando o atleta do banco de dados
        await db_session.delete(atleta)
        # Persistindo as mudanças
        await db_session.commit()
    except Exception as e:
        # Em caso de qualquer outro erro inesperado durante a deleção
        print(f"Erro ao deletar atleta: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro interno ao tentar deletar o atleta."
        )

