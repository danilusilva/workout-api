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

---

## 🔧 Instalação com pip
### Clone o repositório
- git clone https://github.com/seu-usuario/workout-api.git
cd workout-api

### Crie um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt

```
# ▶️ Execução
```bash
uvicorn app.main:app --reload
```
- Acesse a documentação interativa em: http://localhost:8000/docs

---

# 📂 Estrutura do Projeto

```
workout-api/
│
├── app/
│   ├── models/          # Modelos SQLAlchemy
│   ├── schemas/         # Schemas Pydantic
│   ├── routers/         # Rotas organizadas por recurso
│   ├── services/        # Regras de negócio
│   ├── db.py            # Conexão com banco de dados
│   └── main.py          # Inicialização da aplicação FastAPI
│
├── tests/               # Testes automatizados (em breve)
├── requirements.txt     # Dependências
└── README.md            # Documentação
```

# ✨ Contribuição
- Contribuições são muito bem-vindas! Sinta-se livre para abrir issues, sugerir melhorias ou enviar um pull request.


# Desenvolvido por Danilu Silva



