# Testes

Este documento descreve a abordagem de testes para a API de Gerenciamento de Carros, incluindo estratégias, ferramentas e melhores práticas.

## Visão Geral

O projeto possui uma suite de testes automatizados implementada usando Pytest, cobrindo endpoints da API, operações de banco de dados e funcionalidades de segurança.

## Estratégia de Testes

### Tipos de Testes

#### Testes de API
- Testam os endpoints da API diretamente
- Verificam status HTTP, headers e payloads
- Validam autenticação e autorização
- Cobrem operações CRUD completas

#### Testes Unitários
- Testam funções individuais e métodos
- Verificam lógica de negócios isolada
- Testam validações de schemas Pydantic

#### Testes de Integração
- Testam a interação entre diferentes componentes
- Verificam endpoints da API com banco de dados em memória
- Garantem que os diferentes módulos trabalhem juntos corretamente

## Ferramentas de Teste

### Pytest
O framework utilizado para testes é o Pytest, que oferece:

- Simples escrita de testes
- Fixtures para configuração de testes
- Execução seletiva de testes
- Integração com cobertura de código

### Bibliotecas Complementares
- `pytest-asyncio`: Para testes assíncronos
- `httpx`: Para fazer requisições HTTP nos testes de API
- `pytest-cov`: Para medir cobertura de código
- `fastapi.testclient.TestClient`: Cliente de teste para APIs FastAPI

## Estrutura de Testes

### Organização de Arquivos

```
tests/
├── __init__.py
├── conftest.py          # Configuração global dos testes e fixtures
├── test_db.py           # Testes para operações de banco de dados
├── test_auth.py         # Testes para endpoints de autenticação
├── test_users.py        # Testes para endpoints de usuários
├── test_brands.py       # Testes para endpoints de marcas
└── test_cars.py         # Testes para endpoints de carros
```

## Implementação de Testes

### Fixtures

O arquivo `conftest.py` fornece fixtures reutilizáveis:

- `session`: Sessão de banco de dados em memória (SQLite)
- `client`: Cliente de teste FastAPI
- `user_data`: Dados padrão para criação de usuário
- `user`: Usuário criado no banco de dados
- `brand_data`: Dados padrão para criação de marca
- `brand`: Marca criada no banco de dados
- `car_data`: Dados padrão para criação de carro
- `car`: Carro criado no banco de dados
- `auth_headers`: Headers de autenticação com token JWT

### Exemplo de Teste de Criação de Usuário

```python
import pytest
from fastapi import status

class TestCreateUser:
    @pytest.mark.asyncio
    async def test_create_user_success(self, client, user_data):
        response = client.post('/api/v1/users/', json=user_data)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data['username'] == user_data['username']
        assert data['email'] == user_data['email']
        assert 'id' in data
        assert 'created_at' in data
        assert 'update_at' in data
        assert 'password' not in data
```

### Exemplo de Teste de Autenticação

```python
@pytest.mark.asyncio
async def test_login_success(client, user, user_data):
    response = client.post(
        '/api/v1/auth/token',
        json={
            'email': user_data['email'],
            'password': user_data['password'],
        },
    )
    
    assert response.status_code == status.HTTP_200_OK
    assert 'access_token' in response.json()
    assert response.json()['token_type'] == 'bearer'
```

### Exemplo de Teste de Endpoint Protegido

```python
@pytest.mark.asyncio
async def test_list_cars_requires_auth(client):
    response = client.get('/api/v1/cars/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
```

## Configuração de Testes

### Banco de Dados de Teste

O projeto utiliza um banco de dados SQLite em memória para os testes, configurado no `conftest.py`:

```python
@pytest_asyncio.fixture
async def session():
    engine = create_async_engine(url='sqlite+aiosqlite:///:memory:')

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
```

### Client de Teste

O cliente de teste é configurado para sobrescrever a dependência de sessão do banco de dados:

```python
@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()
```

## Execução de Testes

### Comandos Básicos

```bash
# Executar todos os testes
poetry run pytest

# Executar testes com saída verbosa
poetry run pytest -v

# Executar testes com cobertura
poetry run pytest --cov=car_api --cov-report=html --cov-report=term

# Executar testes de um arquivo específico
poetry run pytest tests/test_users.py

# Executar testes de um módulo específico
poetry run pytest tests/test_cars.py -v
```

### Marcadores de Teste

Os testes utilizam marcadores para categorização:

- `@pytest.mark.asyncio`: Para testes assíncronos
- Marcadores personalizados podem ser adicionados para categorizar por tipo (unit, integration, security)

## Cobertura de Testes

### Métricas de Cobertura

Objetivos de cobertura:

- **Mínimo**: 70% de cobertura de código
- **Ideal**: 85% de cobertura de código
- **Crítico**: 95% de cobertura para funções de segurança

### Gerando Relatório de Cobertura

```bash
# Executar testes com cobertura e gerar relatório HTML
poetry run pytest --cov=car_api --cov-report=html

# Abrir o relatório no navegador
# O relatório será gerado em htmlcov/index.html
```

## Melhores Práticas

### Escrita de Testes

- Use nomes descritivos para funções de teste
- Siga o padrão Given-When-Then
- Teste casos de sucesso e erro
- Isole dependências externas quando possível
- Use fixtures para configuração repetida

### Organização

- Mantenha testes perto do código que testam
- Agrupe testes relacionados em classes (ex: `TestCreateUser`, `TestListCars`)
- Evite testes dependentes entre si
- Use fixtures do `conftest.py` para reutilização

### Manutenção

- Atualize testes quando alterar funcionalidades
- Remova testes obsoletos
- Revise testes frágeis regularmente
- Documente cenários complexos de teste

## Testes de Segurança

A suite de testes inclui verificações de segurança:

- Testa acesso não autorizado a endpoints protegidos
- Verifica tratamento adequado de dados sensíveis (senhas não são retornadas)
- Testa validação de entrada contra injeção
- Confirma que tokens expirados ou inválidos são rejeitados

## Melhorias Futuras

1. Configurar CI/CD com execução automática de testes
2. Adicionar testes de carga para endpoints críticos
3. Implementar testes de contrato para API
4. Adicionar testes de desempenho

## Recursos Adicionais

- [Documentação do Pytest](https://docs.pytest.org/)
- [FastAPI Testing Guide](https://fastapi.tiangolo.com/tutorial/testing/)
- [Testing SQLAlchemy with pytest](https://docs.sqlalchemy.org/en/latest/orm/session_transaction.html#testing-with-transactions-and-connection-faq-test)