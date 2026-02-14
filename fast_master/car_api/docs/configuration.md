# Configuração do Projeto

Este documento descreve as configurações necessárias para personalizar o comportamento da API de Gerenciamento de Carros.

## Variáveis de Ambiente

O projeto utiliza o módulo `pydantic-settings` para gerenciar configurações. Todas as configurações são definidas no arquivo `.env` na raiz do projeto.

### Criando o Arquivo .env

Crie um arquivo chamado `.env` na raiz do projeto copiando o modelo `.env.example`:

```bash
cp .env.example .env
```

### Variáveis Disponíveis

#### DATABASE_URL
- **Descrição**: URL de conexão com o banco de dados
- **Tipo**: String
- **Padrão**: `sqlite+aiosqlite:///./car.db`
- **Exemplo**:
  ```
  DATABASE_URL=sqlite+aiosqlite:///./car.db
  ```

#### JWT_SECRET_KEY
- **Descrição**: Chave secreta usada para assinar e verificar tokens JWT
- **Tipo**: String
- **Importância**: **MUITO IMPORTANTE** - Deve ser uma string aleatória e segura
- **Geração**:
  ```bash
  python -c "import secrets; print(secrets.token_urlsafe(32))"
  ```
- **Exemplo**:
  ```
  JWT_SECRET_KEY=seu_valor_secreto_gerado_aqui
  ```

#### JWT_ALGORITHM
- **Descrição**: Algoritmo usado para codificar/decodificar tokens JWT
- **Tipo**: String
- **Padrão**: `HS256`
- **Valores possíveis**: `HS256`, `HS384`, `HS512`
- **Exemplo**:
  ```
  JWT_ALGORITHM=HS256
  ```

#### JWT_EXPIRATION_MINUTES
- **Descrição**: Tempo de expiração do token JWT em minutos
- **Tipo**: Inteiro
- **Padrão**: `30`
- **Exemplo**:
  ```
  JWT_EXPIRATION_MINUTES=30
  ```

## Exemplo Completo do Arquivo .env

```
DATABASE_URL=sqlite+aiosqlite:///./car.db
JWT_SECRET_KEY=gerar_chave_secreta_com_python_secrets
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=30
```

## Configurações do Banco de Dados

### SQLite (padrão)
O projeto vem configurado com SQLite como banco de dados padrão, o que é ideal para desenvolvimento e testes rápidos. O arquivo do banco de dados será criado automaticamente na raiz do projeto.

### PostgreSQL (opcional)
Para usar PostgreSQL, altere a `DATABASE_URL` no arquivo `.env`:

```
DATABASE_URL=postgresql+asyncpg://usuario:senha@localhost:5432/nome_do_banco
```

Certifique-se de instalar as dependências adicionais:
```bash
poetry add asyncpg
```

### MySQL (opcional)
Para usar MySQL, altere a `DATABASE_URL` no arquivo `.env`:

```
DATABASE_URL=mysql+aiomysql://usuario:senha@localhost:3306/nome_do_banco
```

Certifique-se de instalar as dependências adicionais:
```bash
poetry add aiomysql
```

## Configurações de Segurança

### Tempo de Expiração do Token
Ajuste o tempo de expiração do token JWT de acordo com as necessidades de segurança da sua aplicação:

- **Ambientes de desenvolvimento**: Pode ser maior (ex: 60 minutos)
- **Ambientes de produção**: Recomenda-se menor (ex: 15-30 minutos)

### Chave Secreta JWT
- **Importância**: A chave secreta é crucial para a segurança da autenticação
- **Boas práticas**:
  - Use uma chave longa e aleatória (recomendado: 32 bytes ou mais)
  - Não compartilhe a chave em repositórios públicos
  - Altere periodicamente em ambientes de produção
  - Use diferentes chaves para diferentes ambientes

## Configurações do FastAPI

As configurações do FastAPI são definidas no código e não precisam de configuração adicional. No entanto, você pode personalizar o comportamento da aplicação modificando o arquivo `car_api/app.py`.

## Configurações de Logging

O projeto não inclui configurações de logging específicas no momento, mas você pode adicionar conforme necessário. Em ambientes de produção, considere adicionar:

- Nível de log (DEBUG, INFO, WARNING, ERROR)
- Destino do log (arquivo, stdout, serviço externo)
- Formato das mensagens de log

## Configurações de Desenvolvimento vs Produção

### Desenvolvimento
- JWT_EXPIRATION_MINUTES pode ser maior
- Mais logs detalhados podem ser habilitados
- Recursos de debug podem ser ativados

### Produção
- JWT_EXPIRATION_MINUTES deve ser menor
- Banco de dados robusto (PostgreSQL/MySQL) recomendado
- Chave secreta segura e protegida
- Configurações de segurança adicionais

## Migrações de Banco de Dados

O projeto utiliza Alembic para gerenciamento de migrações de banco de dados. Após qualquer alteração nas configurações do banco de dados:

1. Execute as migrações existentes:
   ```bash
   poetry run alembic upgrade head
   ```

2. Se você criou novos modelos, gere uma nova migração:
   ```bash
   poetry run alembic revision --autogenerate -m "descrição_da_migração"
   ```

3. Execute a nova migração:
   ```bash
   poetry run alembic upgrade head
   ```

## Testando as Configurações

Após configurar o ambiente, teste se tudo está funcionando corretamente:

1. Execute a aplicação:
   ```bash
   poetry run fastapi dev car_api/app.py
   ```

2. Acesse `http://localhost:8000/health_check` para verificar o status

3. Verifique os logs para quaisquer mensagens de erro relacionadas à configuração

## Melhores Práticas

- Mantenha o arquivo `.env` fora do controle de versão (já está no `.gitignore`)
- Use diferentes valores para diferentes ambientes (dev, staging, prod)
- Revise regularmente as configurações de segurança
- Documente quaisquer configurações personalizadas adicionais
- Use ferramentas como `python-decouple` ou `django-environ` para facilitar o gerenciamento de configurações em diferentes ambientes