# Pré-requisitos

Antes de instalar e executar a API de Gerenciamento de Carros, certifique-se de que seu sistema atende aos seguintes requisitos:

## Requisitos de Sistema

### Sistema Operacional
- Linux (recomendado)
- macOS
- Windows (com WSL2 recomendado)

### Hardware
- Processador: Dual-core ou superior
- Memória RAM: 4 GB ou mais
- Armazenamento: 500 MB livres para instalação

## Software Necessário

### Python
- **Versão**: Python 3.13 ou superior
- **Verificação**: Execute `python --version` ou `python3 --version`

### Gerenciador de Pacotes
- **Poetry**: Gerenciador de dependências para Python (versão 1.0 ou superior)
- **Instalação do Poetry**: Siga as instruções em https://python-poetry.org/docs/#installation

### Outras Ferramentas
- **Git**: Para clonar o repositório (versão 2.0 ou superior)
- **curl** ou **wget**: Para download de arquivos (opcional, mas recomendado)

## Dependências do Projeto

O projeto utiliza as seguintes bibliotecas e frameworks:

- **FastAPI** (>=0.128.0): Framework web moderno e rápido
- **SQLAlchemy** (>=2.0.46): ORM para interação com banco de dados
- **Pydantic** (>=2.12.5): Validação de dados e serialização
- **PyJWT** (>=2.11.0): Autenticação baseada em tokens JWT
- **Alembic** (>=1.18.3): Migrações de banco de dados
- **Pydantic Settings** (>=2.12.0): Gerenciamento de configurações
- **Argon2** (pwdlib[argon2]): Hash de senhas seguro
- **aiosqlite** (>=0.22.1): Driver assíncrono SQLite

Essas dependências serão instaladas automaticamente pelo Poetry durante a instalação do projeto.

## Conhecimentos Recomendados

Embora não sejam requisitos técnicos, os seguintes conhecimentos ajudarão na compreensão e utilização da API:

- **Python**: Conhecimento intermediário de programação em Python
- **API REST**: Entendimento de conceitos de APIs RESTful
- **JWT**: Conhecimento básico sobre tokens JWT para autenticação
- **SQL**: Conhecimento básico de linguagem SQL para consultas
- **Git**: Controle de versão com Git

## Verificação de Requisitos

Para verificar se os requisitos estão atendidos, execute os seguintes comandos no terminal:

```bash
# Verificar versão do Python
python3 --version

# Verificar se o Poetry está instalado
poetry --version

# Verificar se o Git está instalado
git --version
```

Se todos os comandos retornarem versões válidas, você está pronto para prosseguir com a [instalação](installation.md).