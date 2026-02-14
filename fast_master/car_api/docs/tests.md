# Testes

Este documento descreve a abordagem de testes para a API de Gerenciamento de Carros, incluindo estratégias, ferramentas e melhores práticas.

## Visão Geral

Atualmente, o projeto não inclui testes automatizados implementados, mas esta seção fornece diretrizes para implementação futura de uma suite de testes abrangente.

## Estratégia de Testes

### Tipos de Testes

#### Testes Unitários
- Testam funções individuais e métodos
- Verificam lógica de negócios isolada
- Devem testar validações, funções de utilidade e lógica de segurança

#### Testes de Integração
- Testam a interação entre diferentes componentes
- Verificam endpoints da API com banco de dados real ou simulado
- Garantem que os diferentes módulos trabalhem juntos corretamente

#### Testes de API
- Testam os endpoints da API diretamente
- Verificam status HTTP, headers e payloads
- Validam autenticação e autorização

## Ferramentas de Teste

### Pytest
O framework recomendado para testes é o Pytest, que oferece:

- Simples escrita de testes
- Fixtures para configuração de testes
- Execução paralela de testes
- Integração com cobertura de código

### Bibliotecas Complementares
- `pytest-asyncio`: Para testes assíncronos
- `httpx`: Para fazer requisições HTTP nos testes de API
- `pytest-cov`: Para medir cobertura de código
- `factory-boy`: Para criar dados de teste

## Estrutura de Testes

### Organização de Arquivos

```
tests/
├── __init__.py
├── conftest.py          # Configuração global dos testes
├── test_config.py       # Testes para configurações
├── test_security.py     # Testes para funções de segurança
├── test_database.py     # Testes para operações de banco de dados
├── api/
│   ├── __init__.py
│   ├── test_auth.py     # Testes para endpoints de autenticação
│   ├── test_users.py    # Testes para endpoints de usuários
│   ├── test_brands.py   # Testes para endpoints de marcas
│   └── test_cars.py     # Testes para endpoints de carros
└── factories/
    ├── __init__.py
    ├── user_factory.py  # Factories para criar usuários de teste
    ├── brand_factory.py # Factories para criar marcas de teste
    └── car_factory.py   # Factories para criar carros de teste
```

## Implementação de Testes

### Testes Unitários

Exemplo de teste unitário para uma função de validação:

```python
import pytest
from car_api.schemas.users import UserSchema

def test_username_min_length():
    with pytest.raises(ValueError):
        UserSchema(username="ab", email="test@example.com", password="password123")
```

### Testes de API

Exemplo de teste para endpoint de criação de usuário:

```python
import pytest
from fastapi.testclient import TestClient
from car_api.app import app

@pytest.fixture
def client():
    return TestClient(app)

def test_create_user(client):
    response = client.post("/api/v1/users/", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
```

### Testes de Segurança

Exemplos de testes de segurança:

```python
def test_protected_endpoint_requires_auth(client):
    response = client.get("/api/v1/users/")
    assert response.status_code == 401  # Unauthorized

def test_invalid_token_returns_error(client):
    response = client.get("/api/v1/users/", 
                         headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401
```

## Configuração de Testes

### Banco de Dados de Teste

Use um banco de dados separado para testes:

```python
# conftest.py
import tempfile
import os
from sqlalchemy.ext.asyncio import create_async_engine
from car_api.core.database import engine

@pytest.fixture(scope="session")
def test_db_url():
    # Cria um banco de dados temporário para testes
    temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
    temp_db.close()
    url = f"sqlite+aiosqlite:///{temp_db.name}"
    yield url
    os.unlink(temp_db.name)
```

### Client de Teste

Configure um client de teste para os endpoints:

```python
@pytest.fixture
def client(test_db_session):
    # Sobrescreve a dependência de sessão do banco de dados
    def override_get_session():
        yield test_db_session
    
    app.dependency_overrides[get_session] = override_get_session
    yield TestClient(app)
    app.dependency_overrides.clear()
```

## Cobertura de Testes

### Métricas de Cobertura

Objetivos recomendados de cobertura:

- **Mínimo**: 70% de cobertura de código
- **Ideal**: 85% de cobertura de código
- **Crítico**: 95% de cobertura para funções de segurança

### Execução de Testes com Cobertura

```bash
# Executar testes com cobertura
poetry run pytest --cov=car_api --cov-report=html --cov-report=term

# Executar apenas testes de unidade
poetry run pytest tests/unit/

# Executar apenas testes de API
poetry run pytest tests/api/
```

## Melhores Práticas

### Escrita de Testes

- Use nomes descritivos para funções de teste
- Siga o padrão Given-When-Then
- Teste casos de sucesso e erro
- Isola dependências externas quando possível
- Use fixtures para configuração repetida

### Organização

- Mantenha testes perto do código que testam
- Agrupe testes relacionados
- Use marcadores (markers) para categorizar testes
- Evite testes dependentes entre si

### Manutenção

- Atualize testes quando alterar funcionalidades
- Remova testes obsoletos
- Revise testes frágeis regularmente
- Documente cenários complexos de teste

## Execução de Testes

### Comandos Básicos

```bash
# Executar todos os testes
poetry run pytest

# Executar testes com saída verbosa
poetry run pytest -v

# Executar testes em modo de depuração
poetry run pytest --pdb

# Executar testes de um arquivo específico
poetry run pytest tests/test_users.py

# Executar testes com marcador específico
poetry run pytest -m "integration"
```

### Marcadores de Teste

```python
import pytest

@pytest.mark.unit
def test_create_user_schema():
    # Teste de unidade
    pass

@pytest.mark.integration
def test_create_user_endpoint():
    # Teste de integração
    pass

@pytest.mark.security
def test_auth_required():
    # Teste de segurança
    pass
```

## Testes de Desempenho

### Testes de Carga

Considere adicionar testes de carga para endpoints críticos:

```python
# Exemplo com pytest-benchmark
def test_list_users_performance(benchmark):
    result = benchmark(list_users_function, params={"limit": 100})
    assert len(result) == 100
```

## Testes de Segurança

### Verificação de Vulnerabilidades

Testes que devem ser implementados:

- Tenta acesso não autorizado a endpoints protegidos
- Verifica tratamento adequado de dados sensíveis
- Testa validação de entrada contra injeção
- Confirma que tokens expirados são rejeitados

## Próximos Passos

### Implementação Imediata

1. Criar estrutura básica de testes
2. Implementar testes para funções de segurança
3. Adicionar testes para endpoints de autenticação
4. Criar factories para dados de teste

### Melhorias Futuras

1. Adicionar testes de integração completos
2. Implementar testes de ponta a ponta
3. Configurar CI/CD com execução automática de testes
4. Adicionar testes de segurança automatizados
5. Implementar testes de contrato para API

## Recursos Adicionais

- [Documentação do Pytest](https://docs.pytest.org/)
- [FastAPI Testing Guide](https://fastapi.tiangolo.com/tutorial/testing/)
- [Testing SQLAlchemy with pytest](https://docs.sqlalchemy.org/en/latest/orm/session_transaction.html#testing-with-transactions-and-connection-faq-test)