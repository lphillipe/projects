# API de Gerenciamento de Carros

Bem-vindo à documentação da API de Gerenciamento de Carros, uma aplicação REST desenvolvida com FastAPI e SQLAlchemy para gerenciar veículos, marcas e usuários.

## Visão Geral

Esta API oferece um sistema completo para gerenciamento de carros, permitindo operações CRUD (Criar, Ler, Atualizar e Deletar) para carros, marcas e usuários. A aplicação foi construída com tecnologias modernas e segue práticas recomendadas de desenvolvimento de APIs REST.

### Recursos principais

- **Autenticação e Autorização**: Sistema de autenticação baseado em JWT (JSON Web Tokens)
- **Gestão de Usuários**: Cadastro, edição e exclusão de contas de usuário
- **Gestão de Marcas**: Cadastro e gerenciamento de marcas de veículos
- **Gestão de Carros**: Cadastro e gerenciamento de veículos com informações detalhadas
- **Busca e Filtragem**: Recursos avançados de busca e filtragem para encontrar veículos rapidamente
- **Validação de Dados**: Validações rigorosas para garantir a integridade dos dados
- **Segurança**: Práticas de segurança implementadas para proteger os dados dos usuários

### Tecnologias utilizadas

- **Python 3.13+**: Linguagem principal da aplicação
- **FastAPI**: Framework web moderno e rápido para construção da API
- **SQLAlchemy**: ORM para interação com o banco de dados
- **SQLite**: Banco de dados relacional para armazenamento dos dados
- **Pydantic**: Validação de dados e serialização
- **JWT**: Autenticação baseada em tokens
- **Alembic**: Migrações de banco de dados
- **Pydantic Settings**: Gerenciamento de configurações
- **Argon2**: Hash de senhas seguro

### Benefícios

- **Desempenho**: FastAPI oferece alta performance graças ao suporte nativo a asyncio
- **Documentação Automática**: Integração com Swagger UI e ReDoc para documentação interativa
- **Tipagem Estática**: Suporte a tipagem de dados para melhor manutenção e depuração
- **Escalabilidade**: Arquitetura projetada para escalar conforme necessário
- **Segurança**: Implementação de práticas de segurança para proteger dados sensíveis

## Começando

Para começar a usar esta API, siga os passos descritos na seção de [Instalação](installation.md). Se você estiver interessado em contribuir para o projeto, consulte o guia de [Contribuição](contribution.md).

## Documentação Adicional

- [Pré-requisitos](prerequisites.md)
- [Instalação](installation.md)
- [Configuração do Projeto](configuration.md)
- [Guia de Desenvolvimento](development.md)
- [Endpoints da API](api_endpoints.md)
- [Modelagem do Sistema](system_modeling.md)
- [Autenticação e Segurança](authentication_security.md)
- [Testes](tests.md)
- [Deploy](deploy.md)
- [Diretrizes e Padrões](guidelines.md)
- [Estrutura do Projeto](structure.md)
- [Como Contribuir](contribution.md)
- [Notas de Versão](release_notes.md)