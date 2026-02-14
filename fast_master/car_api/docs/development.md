# Desenvolvimento

Este guia fornece informações essenciais para desenvolvedores que desejam contribuir ou estender a API de Gerenciamento de Carros.

## Ambiente de Desenvolvimento

### Configuração Inicial

1. Clone o repositório:
   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd car_api
   ```

2. Instale as dependências:
   ```bash
   poetry install
   ```

3. Ative o ambiente virtual (opcional):
   ```bash
   poetry shell
   ```

4. Crie o arquivo de ambiente:
   ```bash
   cp .env.example .env
   ```

5. Gere uma chave secreta JWT:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```
   
   Adicione o resultado como valor de `JWT_SECRET_KEY` no arquivo `.env`.

6. Execute as migrações do banco de dados:
   ```bash
   poetry run alembic upgrade head
   ```

### Executando em Modo Desenvolvimento

Para executar a aplicação em modo de desenvolvimento com recarregamento automático:

```bash
poetry run fastapi dev car_api/app.py
```

Ou usando o script definido no `pyproject.toml`:

```bash
poetry run task run
```

A API estará disponível em `http://localhost:8000`.

## Estrutura de Desenvolvimento

### Branches

- `main`: Código estável e em produção
- `develop`: Código em desenvolvimento para próxima release
- `feature/*`: Features em desenvolvimento
- `hotfix/*`: Correções urgentes
- `release/*`: Preparação para releases

### Ciclo de Desenvolvimento

1. Crie uma branch para sua feature ou correção:
   ```bash
   git checkout -b feature/nova-funcionalidade
   ```

2. Implemente suas alterações

3. Execute os testes (quando disponíveis)

4. Formate e verifique o código:
   ```bash
   poetry run task pre_format
   poetry run task lint
   ```

5. Faça commit das alterações:
   ```bash
   git add .
   git commit -m "Descrição clara e concisa das alterações"
   ```

6. Envie para o repositório:
   ```bash
   git push origin feature/nova-funcionalidade
   ```

7. Crie um Pull Request para revisão

## Ferramentas de Desenvolvimento

### Linting e Formatação

O projeto usa Ruff para linting e formatação de código:

- **Verificar problemas**: `poetry run task lint`
- **Formatar automaticamente**: `poetry run task pre_format`
- **Formatação manual**: `poetry run task format`

### Scripts Disponíveis

Scripts definidos no `pyproject.toml`:

- `poetry run task run`: Executa a aplicação em modo de desenvolvimento
- `poetry run task lint`: Verifica problemas de estilo e erros
- `poetry run task pre_format`: Corrige problemas automaticamente
- `poetry run task format`: Formata o código
- `poetry run task docs`: Inicia o servidor de documentação MkDocs

### Documentação Local

Para visualizar a documentação localmente:

```bash
poetry run task docs
```

A documentação estará disponível em `http://127.0.0.1:8001`.

## Desenvolvimento de Funcionalidades

### Adicionando Novos Endpoints

1. Crie o endpoint no roteador apropriado em `car_api/routers/`
2. Defina os esquemas Pydantic em `car_api/schemas/`
3. Atualize os modelos SQLAlchemy em `car_api/models/` se necessário
4. Adicione documentação no endpoint usando decoradores do FastAPI
5. Implemente validações usando Pydantic
6. Teste o endpoint manualmente ou com testes automatizados

### Adicionando Novos Modelos

1. Crie o modelo em `car_api/models/` herdando de `Base`
2. Defina campos com tipos SQLAlchemy apropriados
3. Adicione relacionamentos se necessário
4. Crie esquemas Pydantic correspondentes em `car_api/schemas/`
5. Gere e execute migrações do banco de dados:
   ```bash
   poetry run alembic revision --autogenerate -m "Descrição da mudança"
   poetry run alembic upgrade head
   ```

### Validações Personalizadas

Use validadores Pydantic para validações personalizadas:

```python
from pydantic import field_validator

@field_validator('nome_do_campo')
def validar_nome_do_campo(cls, v):
    # Lógica de validação
    if condição_de_erro:
        raise ValueError('mensagem de erro')
    return v
```

## Banco de Dados

### Migrações

O projeto usa Alembic para gerenciamento de migrações:

- **Gerar migração**: `poetry run alembic revision --autogenerate -m "descrição"`
- **Aplicar migrações**: `poetry run alembic upgrade head`
- **Reverter migração**: `poetry run alembic downgrade -1`

### Consultas Assíncronas

Todas as operações de banco de dados são assíncronas:

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

async def minha_funcao(db: AsyncSession):
    result = await db.execute(select(MeuModelo))
    itens = result.scalars().all()
    return itens
```

## Debugging

### Logging

Embora o projeto não tenha logging extensivo implementado, você pode adicionar conforme necessário:

```python
import logging

logger = logging.getLogger(__name__)

def minha_funcao():
    logger.info("Mensagem de informação")
    logger.error("Mensagem de erro")
```

### Depuração com Print

Durante o desenvolvimento, você pode usar prints para depuração temporária:

```python
def minha_funcao(parametro):
    print(f"Parâmetro recebido: {parametro}")
    # resto da função
```

Lembre-se de remover prints de depuração antes de fazer commit.

## Melhores Práticas de Desenvolvimento

### Código Limpo

- Use nomes descritivos para variáveis, funções e classes
- Mantenha funções pequenas e com responsabilidade única
- Evite duplicação de código
- Comente decisões complexas ou não óbvias

### Segurança

- Sempre valide dados de entrada
- Use SQLAlchemy para evitar SQL injection
- Implemente controle de acesso adequado
- Não exponha informações sensíveis nos logs

### Performance

- Use eager loading para evitar N+1 queries
- Implemente paginação para listagens grandes
- Considere caching para dados que não mudam frequentemente
- Otimize consultas com filtros e índices

## Recursos Úteis

### Documentação da API

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Ferramentas Externas

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)

## Solução de Problemas Comuns

### Problemas com Dependências

Se encontrar problemas com dependências:

1. Limpe o cache do Poetry:
   ```bash
   poetry cache clear pypi --all
   ```

2. Remova o ambiente virtual e crie novamente:
   ```bash
   poetry env remove python
   poetry install
   ```

### Problemas com Banco de Dados

Se encontrar problemas com o banco de dados:

1. Verifique se o caminho do banco de dados é acessível
2. Execute migrações novamente:
   ```bash
   poetry run alembic upgrade head
   ```

### Problemas com Tokens JWT

Se encontrar problemas com autenticação:

1. Verifique se `JWT_SECRET_KEY` está correta no `.env`
2. Confirme que o token não expirou
3. Verifique se o formato do token está correto (Bearer {token})

## Contribuindo

Siga as diretrizes em [Como Contribuir](contribution.md) para enviar suas contribuições.

## Próximos Passos

Depois de configurar seu ambiente de desenvolvimento:

1. Explore os endpoints existentes
2. Execute a aplicação e experimente os recursos
3. Leia a documentação dos endpoints
4. Comece com pequenas melhorias ou correções de bugs
5. Participe das discussões sobre novas funcionalidades