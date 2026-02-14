# Estrutura do Projeto

Este documento descreve a estrutura de diretórios e arquivos do projeto API de Gerenciamento de Carros, explicando a organização e a finalidade de cada componente.

## Estrutura de Diretórios

```
car_api/
├── __init__.py
├── app.py
├── core/
│   ├── __init__.py
│   ├── database.py
│   ├── security.py
│   └── settings.py
├── models/
│   ├── __init__.py
│   ├── base.py
│   ├── cars.py
│   └── users.py
├── routers/
│   ├── __init__.py
│   ├── auth.py
│   ├── brands.py
│   ├── cars.py
│   └── users.py
└── schemas/
    ├── __init__.py
    ├── auth.py
    ├── brands.py
    ├── cars.py
    └── users.py
```

## Descrição dos Diretórios

### Raiz do Projeto (`/`)

- **`.env`**: Arquivo de configurações de ambiente (não versionado)
- **`.env.example`**: Modelo com variáveis de ambiente disponíveis
- **`alembic.ini`**: Configuração do Alembic para migrações de banco de dados
- **`car.db`**: Arquivo do banco de dados SQLite (padrão)
- **`mkdocs.yml`**: Configuração da documentação MkDocs
- **`poetry.lock`**: Lock file do Poetry com versões exatas das dependências
- **`pyproject.toml`**: Configuração do projeto Python e dependências
- **`README.md`**: Documentação inicial do projeto
- **`car_api/`**: Diretório principal da aplicação
- **`docs/`**: Documentação do projeto
- **`migrations/`**: Scripts de migração do banco de dados
- **`tests/`**: Testes automatizados

### Diretório Principal (`car_api/`)

- **`__init__.py`**: Arquivo de inicialização do pacote
- **`app.py`**: Ponto de entrada da aplicação FastAPI

### Diretório Core (`car_api/core/`)

Componentes centrais da aplicação:

- **`database.py`**: Configuração e conexão com o banco de dados
- **`security.py`**: Funções de segurança (autenticação, hashing de senha, JWT)
- **`settings.py`**: Configurações da aplicação usando Pydantic Settings

### Diretório Models (`car_api/models/`)

Modelos de dados do SQLAlchemy:

- **`base.py`**: Classe base para todos os modelos
- **`cars.py`**: Modelos relacionados a carros e marcas
- **`users.py`**: Modelo de usuário

### Diretório Routers (`car_api/routers/`)

Rotas e endpoints da API:

- **`auth.py`**: Endpoints de autenticação (login, refresh token)
- **`brands.py`**: Endpoints de marcas de carros (CRUD)
- **`cars.py`**: Endpoints de carros (CRUD)
- **`users.py`**: Endpoints de usuários (CRUD)

### Diretório Schemas (`car_api/schemas/`)

Esquemas Pydantic para validação de dados:

- **`auth.py`**: Esquemas para autenticação
- **`brands.py`**: Esquemas para marcas de carros
- **`cars.py`**: Esquemas para carros
- **`users.py`**: Esquemas para usuários

## Descrição Detalhada dos Arquivos

### `car_api/app.py`

Arquivo principal da aplicação FastAPI. Define a instância do FastAPI e inclui todos os roteadores. Também define um endpoint de health check para verificação de status.

### `car_api/core/database.py`

Contém a configuração do motor de banco de dados SQLAlchemy e a função geradora de sessões assíncronas.

### `car_api/core/security.py`

Funções de segurança como autenticação de usuário, criação e verificação de tokens JWT, e hashing de senhas.

### `car_api/core/settings.py`

Define as configurações da aplicação usando Pydantic Settings, carregando variáveis do ambiente.

### `car_api/models/cars.py`

Define os modelos SQLAlchemy para Car e Brand, incluindo campos, relacionamentos e enums para tipos de combustível e transmissão.

### `car_api/models/users.py`

Define o modelo SQLAlchemy para User, incluindo campos e relacionamentos com carros.

### `car_api/routers/auth.py`

Contém endpoints para geração e renovação de tokens JWT.

### `car_api/routers/users.py`

Contém endpoints CRUD para gerenciamento de usuários.

### `car_api/routers/brands.py`

Contém endpoints CRUD para gerenciamento de marcas de carros.

### `car_api/routers/cars.py`

Contém endpoints CRUD para gerenciamento de carros.

### `car_api/schemas/auth.py`

Define esquemas Pydantic para requisições e respostas de autenticação.

### `car_api/schemas/users.py`

Define esquemas Pydantic para requisições e respostas de operações com usuários.

### `car_api/schemas/brands.py`

Define esquemas Pydantic para requisições e respostas de operações com marcas.

### `car_api/schemas/cars.py`

Define esquemas Pydantic para requisições e respostas de operações com carros.

## Diretórios Especiais

### `migrations/`

Contém os scripts de migração gerados pelo Alembic para evolução do schema do banco de dados.

### `tests/`

Destinado a conter os testes automatizados da aplicação (ainda não implementado no projeto atual).

### `docs/`

Contém a documentação do projeto em formato Markdown.

## Arquivos de Configuração

### `pyproject.toml`

Arquivo de configuração do projeto Python que define dependências, scripts e configurações de formatação.

### `alembic.ini`

Arquivo de configuração do Alembic que define como as migrações são geradas e aplicadas.

### `mkdocs.yml`

Arquivo de configuração para geração da documentação estática usando MkDocs.

## Considerações de Arquitetura

A estrutura do projeto segue princípios de arquitetura limpa e separação de responsabilidades:

- **Separação de Camadas**: A aplicação é dividida em camadas distintas (rotas, modelos, esquemas, lógica de negócio)
- **Inversão de Dependência**: Uso de injeção de dependência para conexão com o banco de dados
- **Configuração Centralizada**: Todas as configurações estão centralizadas em `settings.py`
- **Validação de Dados**: Todos os dados de entrada e saída são validados usando Pydantic
- **Segurança Integrada**: A lógica de segurança está isolada em seu próprio módulo

Essa estrutura permite fácil manutenção, testabilidade e escalabilidade da aplicação.