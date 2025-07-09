# 🏋️ Workout API

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red)
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)
![License](https://img.shields.io/badge/license-MIT-blue)

Uma API robusta para gerenciar **atletas**, **categorias de treino** e **centros de treinamento**, desenvolvida com **FastAPI**, **SQLAlchemy** e **Pydantic**.

---

## 🚀 Funcionalidades

### 👤 Gestão de Atletas

- ✅ **Criação**: Adiciona um ou múltiplos atletas com validação de dados (incluindo CPF único).
- 🔍 **Listagem**: Consulta todos os atletas cadastrados.
- 🔎 **Busca por ID**: Recupera informações detalhadas de um atleta específico.
- ✏️ **Atualização**: Modifica dados de um atleta existente.
- 🗑️ **Exclusão**: Remove um atleta do sistema.

---

### 🏷️ Gestão de Categorias

- ✅ **Criação**: Adiciona novas categorias de treino.
- 🔍 **Listagem**: Consulta todas as categorias.
- 🔎 **Busca por ID**: Recupera uma categoria específica.
- 🗑️ **Exclusão**: Remove uma categoria (com verificação de atletas vinculados para manter a integridade dos dados).

---

### 🏢 Gestão de Centros de Treinamento

- ✅ **Criação**: Adiciona novos centros de treinamento.
- 🔍 **Listagem**: Consulta todos os centros.
- 🔎 **Busca por ID**: Recupera um centro específico.
- 🗑️ **Exclusão**: Remove um centro de treinamento (com verificação de atletas vinculados).

---

## ✅ Recursos Adicionais

- 🛡️ **Validação de Dados**: Utiliza Pydantic para garantir a integridade e o formato correto dos dados.
- 📦 **Respostas Padronizadas**: Todas as respostas seguem o seguinte formato:

```
{
  "success": true,
  "data": {...},
  "error": null
}
```
---

## 🛠️ Instalação e Execução
### Pré-requisitos
- Python 3.11+
- Git
- Gerenciador de pacotes pip ou poetry
- Docker
- SGBD para gerenciar informações(Utilizei DBeaver, conectado com PostgreeSQL)
- Alembic para migrar dados

---

## 🔧 Instalação com pip

```bash

# Clone o repositório
- git clone https://github.com/danilusilva/workout-api.git

# Mova-se para o diretório da API
cd workout-api

# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente virtual
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt

# Inicie a imagem no Docker/inicie o contêiner Docker
docker compose up -d

# Migre os dados já existentes com alembic
alembic upgrade head

```
# ▶️ Execução
```bash
uvicorn workout_api.main:app --reload
```
- Acesse a documentação interativa em: http://localhost:8000/docs

---

# 📂 Estrutura do Projeto

```
workout-api/
│
├── .venv/                   # Ambiente virtual (Ao ser criado essa pasta surge)
├── alembic/                 # Ferramenta de migração de banco de dados
│   └── (arquivos do Alembic)
├── workout_api/             # Código-fonte da API
│   └── (módulos Python)
├── .gitignore               # Arquivos e diretórios a serem ignorados pelo Git
├── alembic.ini              # Arquivo de configuração do Alembic
├── docker-compose.yml       # Configuração para Docker Compose
├── Makefile                 # Arquivo para automação de tarefas
├── README.md                # Documentação do projeto
└── requirements.txt         # Dependências do Python
```

# ✨ Contribuição
- Contribuições são muito bem-vindas! Sinta-se livre para abrir issues, sugerir melhorias ou enviar um pull request.


# Desenvolvido por Danilu Silva



