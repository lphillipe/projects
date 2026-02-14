# Instalação

Este guia irá orientá-lo através do processo de instalação da API de Gerenciamento de Carros em seu ambiente local.

## Clonando o Repositório

Primeiro, clone o repositório para sua máquina local:

```bash
git clone <URL_DO_REPOSITORIO>
cd car_api
```

Substitua `<URL_DO_REPOSITORIO>` pela URL real do repositório.

## Configurando o Ambiente Virtual

Este projeto utiliza Poetry para gerenciamento de dependências. Siga os passos abaixo para configurar o ambiente:

### 1. Instalando as dependências

Execute o comando abaixo para instalar todas as dependências do projeto:

```bash
poetry install
```

Este comando irá:
- Criar um ambiente virtual isolado (opcionalmente)
- Instalar todas as dependências listadas no arquivo `pyproject.toml`
- Instalar também as dependências de desenvolvimento

### 2. Ativando o ambiente virtual (opcional)

Se desejar trabalhar dentro do ambiente virtual criado pelo Poetry:

```bash
poetry shell
```

Alternativamente, você pode executar comandos dentro do ambiente virtual usando:

```bash
poetry run <comando>
```

## Configuração Inicial

### 1. Criando o arquivo .env

Copie o arquivo de exemplo de variáveis de ambiente:

```bash
cp .env.example .env
```

Em seguida, edite o arquivo `.env` com suas configurações específicas (veja a seção de [Configuração do Projeto](configuration.md) para detalhes).

### 2. Gerando uma chave secreta JWT

Para autenticação segura, gere uma chave secreta JWT forte:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Adicione o resultado como valor da variável `JWT_SECRET_KEY` no arquivo `.env`.

### 3. Executando migrações do banco de dados

Execute as migrações iniciais para criar as tabelas necessárias:

```bash
poetry run alembic upgrade head
```

## Executando a Aplicação

### Modo de Desenvolvimento

Para executar a aplicação em modo de desenvolvimento com recarregamento automático:

```bash
poetry run fastapi dev car_api/app.py
```

Ou alternativamente, usando o script definido no `pyproject.toml`:

```bash
poetry run task run
```

### Modo de Produção

Para executar em modo de produção (sem recarregamento automático):

```bash
poetry run uvicorn car_api.app:app --host 0.0.0.0 --port 8000
```

## Verificando a Instalação

Após iniciar a aplicação, você pode verificar se tudo está funcionando corretamente:

1. Acesse `http://localhost:8000/health_check` para verificar o status da aplicação
2. Acesse `http://localhost:8000/docs` para visualizar a documentação interativa da API (Swagger UI)
3. Acesse `http://localhost:8000/redoc` para visualizar a documentação em formato ReDoc

## Solução de Problemas

### Problemas Comuns

1. **Erro ao instalar dependências com Poetry**:
   - Certifique-se de que está usando uma versão compatível do Python (3.13+)
   - Tente limpar o cache do Poetry: `poetry cache clear pypi --all`

2. **Erro de banco de dados ao executar migrações**:
   - Verifique se o caminho do banco de dados especificado em `.env` é válido e acessível
   - Confirme que o diretório existe e tem permissões adequadas

3. **Porta já em uso**:
   - Altere a porta no comando de execução ou verifique se outro processo já está utilizando a porta 8000

### Verificando Versões

Certifique-se de que está usando as versões corretas das ferramentas:

```bash
# Verificar versão do Python
python3 --version

# Verificar versão do Poetry
poetry --version

# Verificar versão do Alembic
poetry run alembic --version
```

## Próximos Passos

Agora que a instalação está concluída, você pode:

- Explorar os [Endpoints da API](api_endpoints.md)
- Configurar o ambiente de acordo com suas necessidades (veja [Configuração do Projeto](configuration.md))
- Começar a desenvolver novas funcionalidades (veja [Guia de Desenvolvimento](development.md))
- Executar os testes para garantir que tudo está funcionando corretamente (veja [Testes](tests.md))