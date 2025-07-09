# Makefile (versão aprimorada com pré-requisitos)

PYTHON_ENV_DIR = .venv
APP_MODULE = workout_api.main:app

.PHONY: run create-migrations run-migrations install

# Adicione esta tarefa para instalar dependências
install:
	@echo "Verificando/instalando ambiente virtual e dependências..."
	@if [ ! -d "$(PYTHON_ENV_DIR)" ]; then python -m venv $(PYTHON_ENV_DIR); fi
	$(PYTHON_ENV_DIR)/bin/pip install -r requirements.txt

run: install # Certifica que as dependências estão instaladas antes de rodar
	@echo "Rodando a API localmente..."
	@$(PYTHON_ENV_DIR)/bin/uvicorn $(APP_MODULE) --reload --host 0.0.0.0 --port 8000

# Usando $(shell pwd) para garantir que PYTHONPATH seja resolvido corretamente
# E $(MSG) para a mensagem da migração
create-migrations: install # Instala antes de rodar alembic
	@echo "Criando nova migração Alembic..."
	@PYTHONPATH=$(shell pwd) $(PYTHON_ENV_DIR)/bin/alembic revision --autogenerate -m "$(MSG)"

run-migrations: install # Instala antes de rodar alembic
	@echo "Aplicando migrações Alembic..."
	@PYTHONPATH=$(shell pwd) $(PYTHON_ENV_DIR)/bin/alembic upgrade head

# Exemplo de uso: make create-migrations MSG="add user table"
# Exemplo de uso: make run
# Exemplo de uso: make run-migrations