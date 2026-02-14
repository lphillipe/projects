# Autenticação e Segurança

Este documento detalha os mecanismos de autenticação e segurança implementados na API de Gerenciamento de Carros.

## Visão Geral

A API implementa um sistema de autenticação baseado em JWT (JSON Web Tokens) para proteger os endpoints e garantir que apenas usuários autorizados possam acessar recursos específicos. O sistema também inclui práticas de segurança para proteger contra ameaças comuns.

## Autenticação

### JWT (JSON Web Tokens)

O sistema utiliza tokens JWT para autenticação stateless. Isso significa que o servidor não precisa manter sessões ativas, tornando o sistema mais escalável.

#### Estrutura do Token

Um token JWT típico tem três partes separadas por pontos:

1. **Header**: Contém o tipo de token e o algoritmo de criptografia
2. **Payload**: Contém as claims (informações sobre o usuário)
3. **Signature**: Verifica a integridade do token

#### Claims do Payload

- `sub`: Subject (ID do usuário)
- `exp`: Timestamp de expiração do token

### Processo de Autenticação

1. **Login**: O usuário envia email e senha para `/api/v1/auth/token`
2. **Verificação**: As credenciais são verificadas no banco de dados
3. **Geração de Token**: Um token JWT é gerado com o ID do usuário
4. **Retorno**: O token é retornado ao cliente
5. **Uso Subsequente**: O cliente inclui o token no header Authorization para acessar endpoints protegidos

### Expiração de Tokens

Por padrão, os tokens expiram após 30 minutos (configurável em `JWT_EXPIRATION_MINUTES`). Isso ajuda a minimizar o risco de tokens comprometidos serem usados por longos períodos.

### Atualização de Tokens

A API fornece um endpoint para atualizar tokens próximos do vencimento:

- **Endpoint**: `POST /api/v1/auth/refresh_token`
- **Requisito**: Token JWT válido no header de autorização
- **Resultado**: Novo token JWT com novo tempo de expiração

## Segurança

### Hashing de Senhas

As senhas são armazenadas com hashing seguro usando Argon2 através da biblioteca `pwdlib`. Isso garante que mesmo que o banco de dados seja comprometido, as senhas dos usuários permaneçam protegidas.

### Validação de Tokens

Todos os endpoints protegidos verificam a validade do token JWT antes de executar qualquer operação:

- Verificação da assinatura do token
- Verificação de expiração
- Verificação de ID de usuário válido no banco de dados

### Controle de Acesso

Além da autenticação básica, o sistema implementa controle de acesso refinado:

- **Proprietário de Carro**: Somente o proprietário pode editar ou excluir seus próprios carros
- **Permissões de Marca**: Apenas usuários autenticados podem gerenciar marcas
- **Restrições de Dados**: Verificação de unicidade para campos críticos (placas, emails, usernames)

### Proteção contra Ataques

#### SQL Injection

O uso do SQLAlchemy com consultas parametrizadas previne SQL injection.

#### Validação de Dados

Todos os dados de entrada são validados usando Pydantic, que inclui:

- Validação de formato de email
- Limites numéricos e de tamanho
- Tipos de dados específicos
- Validação personalizada para campos críticos

#### Rate Limiting

Embora não implementado no código atual, recomenda-se adicionar rate limiting para proteger contra tentativas de força bruta.

## Configurações de Segurança

### Variáveis de Ambiente

As configurações de segurança são gerenciadas por variáveis de ambiente:

- `JWT_SECRET_KEY`: Chave secreta para assinar tokens (deve ser mantida segura!)
- `JWT_ALGORITHM`: Algoritmo de criptografia (padrão: HS256)
- `JWT_EXPIRATION_MINUTES`: Tempo de expiração do token (padrão: 30)

### Boas Práticas de Segurança

#### Chave Secreta JWT

- Use uma chave longa e aleatória (recomendado: 32 bytes ou mais)
- Não compartilhe a chave em repositórios públicos
- Altere periodicamente em ambientes de produção
- Use diferentes chaves para diferentes ambientes

#### Ambientes de Produção

- Use HTTPS obrigatoriamente
- Configure cabeçalhos de segurança HTTP (HSTS, CSP, etc.)
- Implemente logging de eventos de segurança
- Monitore tentativas de acesso não autorizado
- Use banco de dados robusto (PostgreSQL/MySQL) em vez de SQLite

## Implementação Técnica

### Módulo de Segurança

O código de segurança está localizado em `car_api/core/security.py` e inclui:

- Funções para hashing e verificação de senhas
- Criação e verificação de tokens JWT
- Função de autenticação de usuário
- Middleware de obtenção do usuário atual
- Função de verificação de propriedade de carro

### Dependências de Segurança

- `pwdlib[argon2]`: Para hashing seguro de senhas
- `pyjwt`: Para geração e verificação de tokens JWT
- `fastapi.security`: Para implementação de esquemas de segurança

## Considerações de Segurança Adicionais

### Auditoria

Embora não implementado no código atual, considere adicionar auditoria para:

- Tentativas de login falhas
- Acessos a dados sensíveis
- Modificações em dados críticos

### Monitoramento

Implemente monitoramento para detectar:

- Padrões incomuns de acesso
- Tentativas de força bruta
- Uso de tokens inválidos ou expirados

### Política de Senhas

Embora validação mínima esteja implementada, considere políticas mais rigorosas:

- Complexidade mínima (maiúsculas, minúsculas, números, símbolos)
- Histórico de senhas para evitar reutilização
- Expiração de senhas periódica

## Melhorias de Segurança Futuras

### Autenticação de Dois Fatores (2FA)

Considere implementar 2FA para contas de usuário, especialmente para operações sensíveis.

### Refresh Tokens

Implementar refresh tokens para melhor gerenciamento de sessão, permitindo invalidação de tokens sem exigir novo login.

### Criptografia de Dados Sensíveis

Para dados particularmente sensíveis, considere criptografia adicional no nível de aplicação.

### Política de Rotatividade de Chaves

Implementar rotação periódica de chaves JWT para aumentar a segurança.

## Testes de Segurança

Embora não implementados no projeto atual, recomenda-se desenvolver testes de segurança para:

- Verificar proteção de endpoints
- Validar tratamento de tokens inválidos
- Testar limites de validação
- Verificar controle de acesso adequado