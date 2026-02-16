# API Endpoints

Esta seção documenta todos os endpoints da API de Gerenciamento de Carros, incluindo métodos HTTP, parâmetros, exemplos de requisição e resposta.

## Visão Geral

- **Base URL**: `http://localhost:8000` (em desenvolvimento)
- **Prefixo da API**: `/api/v1/`
- **Autenticação**: JWT Bearer Token (exceto endpoints públicos)
- **Content-Type**: `application/json`

## Endpoints de Autenticação

### Gerar Token de Acesso
- **Endpoint**: `POST /api/v1/auth/token`
- **Descrição**: Autentica um usuário e retorna um token JWT
- **Autenticação**: Pública

#### Parâmetros
```json
{
  "email": "string",
  "password": "string"
}
```

#### Exemplo de Requisição
```bash
curl -X POST "http://localhost:8000/api/v1/auth/token" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@example.com",
    "password": "senha123"
  }'
```

#### Exemplo de Resposta (200 OK)
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### Erros Possíveis
- 401: Credenciais inválidas

### Atualizar Token de Acesso
- **Endpoint**: `POST /api/v1/auth/refresh_token`
- **Descrição**: Renova um token JWT existente
- **Autenticação**: JWT Bearer Token necessário

#### Exemplo de Requisição
```bash
curl -X POST "http://localhost:8000/api/v1/auth/refresh_token" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

#### Exemplo de Resposta (200 OK)
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

## Endpoints de Usuários

### Criar Novo Usuário
- **Endpoint**: `POST /api/v1/users/`
- **Descrição**: Cria um novo usuário
- **Autenticação**: Pública

#### Parâmetros
```json
{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

#### Validações
- Username: mínimo de 3 caracteres
- Email: formato de email válido
- Password: mínimo de 6 caracteres

#### Exemplo de Requisição
```bash
curl -X POST "http://localhost:8000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "joaosilva",
    "email": "joao@example.com",
    "password": "senha123"
  }'
```

#### Exemplo de Resposta (201 Created)
```json
{
  "id": 1,
  "username": "joaosilva",
  "email": "joao@example.com",
  "created_at": "2023-01-01T00:00:00",
  "update_at": "2023-01-01T00:00:00"
}
```

#### Erros Possíveis
- 400: Username ou email já em uso

### Listar Usuários
- **Endpoint**: `GET /api/v1/users/`
- **Descrição**: Retorna uma lista de usuários
- **Autenticação**: JWT Bearer Token necessário

#### Parâmetros de Query
- `offset` (opcional): Número de registros para pular (padrão: 0)
- `limit` (opcional): Limite de registros (padrão: 100, máximo: 100)
- `search` (opcional): Buscar por username ou email

#### Exemplo de Requisição
```bash
curl -X GET "http://localhost:8000/api/v1/users/?offset=0&limit=10&search=joao" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

#### Exemplo de Resposta (200 OK)
```json
{
  "users": [
    {
      "id": 1,
      "username": "joaosilva",
      "email": "joao@example.com",
      "created_at": "2023-01-01T00:00:00",
      "update_at": "2023-01-01T00:00:00"
    }
  ],
  "offset": 0,
  "limit": 10
}
```

### Buscar Usuário por ID
- **Endpoint**: `GET /api/v1/users/{user_id}`
- **Descrição**: Retorna os detalhes de um usuário específico
- **Autenticação**: JWT Bearer Token necessário

#### Parâmetros
- `user_id`: ID do usuário

#### Exemplo de Requisição
```bash
curl -X GET "http://localhost:8000/api/v1/users/1" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

#### Exemplo de Resposta (200 OK)
```json
{
  "id": 1,
  "username": "joaosilva",
  "email": "joao@example.com",
  "created_at": "2023-01-01T00:00:00",
  "update_at": "2023-01-01T00:00:00"
}
```

#### Erros Possíveis
- 404: Usuário não encontrado

### Atualizar Usuário
- **Endpoint**: `PUT /api/v1/users/{user_id}`
- **Descrição**: Atualiza os dados de um usuário
- **Autenticação**: JWT Bearer Token necessário

#### Parâmetros
- `user_id`: ID do usuário
- Corpo da requisição (campos opcionais):
```json
{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

#### Exemplo de Requisição
```bash
curl -X PUT "http://localhost:8000/api/v1/users/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -d '{
    "username": "joaosilvaneto"
  }'
```

#### Exemplo de Resposta (201 Created)
```json
{
  "id": 1,
  "username": "joaosilvaneto",
  "email": "joao@example.com",
  "created_at": "2023-01-01T00:00:00",
  "update_at": "2023-01-02T00:00:00"
}
```

#### Erros Possíveis
- 400: Username ou email já em uso
- 404: Usuário não encontrado

### Deletar Usuário
- **Endpoint**: `DELETE /api/v1/users/{user_id}`
- **Descrição**: Remove um usuário
- **Autenticação**: JWT Bearer Token necessário

#### Parâmetros
- `user_id`: ID do usuário

#### Exemplo de Requisição
```bash
curl -X DELETE "http://localhost:8000/api/v1/users/1" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

#### Exemplo de Resposta (204 No Content)

#### Erros Possíveis
- 404: Usuário não encontrado

## Endpoints de Marcas

### Criar Nova Marca
- **Endpoint**: `POST /api/v1/brands/`
- **Descrição**: Cria uma nova marca de carro
- **Autenticação**: JWT Bearer Token necessário

#### Parâmetros
```json
{
  "name": "string",
  "description": "string",
  "is_active": "boolean"
}
```

#### Validações
- Name: mínimo de 2 caracteres

#### Exemplo de Requisição
```bash
curl -X POST "http://localhost:8000/api/v1/brands/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -d '{
    "name": "Volkswagen",
    "description": "Fabricante alemão de veículos",
    "is_active": true
  }'
```

#### Exemplo de Resposta (201 Created)
```json
{
  "id": 1,
  "name": "Volkswagen",
  "description": "Fabricante alemão de veículos",
  "is_active": true,
  "created_at": "2023-01-01T00:00:00",
  "update_at": "2023-01-01T00:00:00"
}
```

#### Erros Possíveis
- 400: Nome da marca já em uso

### Listar Marcas
- **Endpoint**: `GET /api/v1/brands/`
- **Descrição**: Retorna uma lista de marcas
- **Autenticação**: JWT Bearer Token necessário

#### Parâmetros de Query
- `offset` (opcional): Número de registros para pular (padrão: 0)
- `limit` (opcional): Limite de registros (padrão: 100, máximo: 100)
- `search` (opcional): Buscar por nome da marca
- `is_active` (opcional): Filtrar por marcas ativas

#### Exemplo de Requisição
```bash
curl -X GET "http://localhost:8000/api/v1/brands/?offset=0&limit=10&search=vw&is_active=true" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

#### Exemplo de Resposta (200 OK)
```json
{
  "brands": [
    {
      "id": 1,
      "name": "Volkswagen",
      "description": "Fabricante alemão de veículos",
      "is_active": true,
      "created_at": "2023-01-01T00:00:00",
      "update_at": "2023-01-01T00:00:00"
    }
  ],
  "offset": 0,
  "limit": 10
}
```

### Buscar Marca por ID
- **Endpoint**: `GET /api/v1/brands/{brand_id}`
- **Descrição**: Retorna os detalhes de uma marca específica
- **Autenticação**: JWT Bearer Token necessário

#### Parâmetros
- `brand_id`: ID da marca

#### Exemplo de Requisição
```bash
curl -X GET "http://localhost:8000/api/v1/brands/1" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

#### Exemplo de Resposta (200 OK)
```json
{
  "id": 1,
  "name": "Volkswagen",
  "description": "Fabricante alemão de veículos",
  "is_active": true,
  "created_at": "2023-01-01T00:00:00",
  "update_at": "2023-01-01T00:00:00"
}
```

#### Erros Possíveis
- 404: Marca não encontrada

### Atualizar Marca
- **Endpoint**: `PUT /api/v1/brands/{brand_id}`
- **Descrição**: Atualiza os dados de uma marca
- **Autenticação**: JWT Bearer Token necessário

#### Parâmetros
- `brand_id`: ID da marca
- Corpo da requisição (campos opcionais):
```json
{
  "name": "string",
  "description": "string",
  "is_active": "boolean"
}
```

#### Exemplo de Requisição
```bash
curl -X PUT "http://localhost:8000/api/v1/brands/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -d '{
    "name": "Volkswagen AG",
    "description": "Empresa automotiva alemã"
  }'
```

#### Exemplo de Resposta (200 OK)
```json
{
  "id": 1,
  "name": "Volkswagen AG",
  "description": "Empresa automotiva alemã",
  "is_active": true,
  "created_at": "2023-01-01T00:00:00",
  "update_at": "2023-01-02T00:00:00"
}
```

#### Erros Possíveis
- 400: Nome da marca já em uso
- 404: Marca não encontrada

### Deletar Marca
- **Endpoint**: `DELETE /api/v1/brands/{brand_id}`
- **Descrição**: Remove uma marca
- **Autenticação**: JWT Bearer Token necessário

#### Parâmetros
- `brand_id`: ID da marca

#### Exemplo de Requisição
```bash
curl -X DELETE "http://localhost:8000/api/v1/brands/1" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

#### Exemplo de Resposta (204 No Content)

#### Erros Possíveis
- 400: Não é possível deletar marca que possui carros associados
- 404: Marca não encontrada

## Endpoints de Carros

### Criar Novo Carro
- **Endpoint**: `POST /api/v1/cars/`
- **Descrição**: Cria um novo carro
- **Autenticação**: JWT Bearer Token necessário

#### Parâmetros
```json
{
  "model": "string",
  "factory_year": "integer",
  "model_year": "integer",
  "color": "string",
  "plate": "string",
  "fuel_type": "string",
  "transmission": "string",
  "price": "decimal",
  "description": "string",
  "is_available": "boolean",
  "brand_id": "integer",
  "owner_id": "integer"
}
```

#### Tipos de Combustível Válidos
- `gasoline` (gasolina)
- `ethanol` (etanol)
- `flex` (flex)
- `diesel` (diesel)
- `electric` (elétrico)
- `hybrid` (hibrido)

#### Tipos de Transmissão Válidos
- `manual`
- `automatic`
- `semi_automatic`
- `cvt`

#### Validações
- Model: mínimo de 2 caracteres
- Color: mínimo de 2 caracteres
- Plate: entre 7 e 10 caracteres
- Factory_year e Model_year: entre 1900 e 2030
- Price: maior que zero

#### Exemplo de Requisição
```bash
curl -X POST "http://localhost:8000/api/v1/cars/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -d '{
    "model": "Golf",
    "factory_year": 2020,
    "model_year": 2021,
    "color": "Branco",
    "plate": "ABC1D23",
    "fuel_type": "flex",
    "transmission": "automatic",
    "price": 85000.00,
    "description": "Excelente estado",
    "is_available": true,
    "brand_id": 1,
    "owner_id": 1
  }'
```

#### Exemplo de Resposta (201 Created)
```json
{
  "id": 1,
  "model": "Golf",
  "factory_year": 2020,
  "model_year": 2021,
  "color": "Branco",
  "plate": "ABC1D23",
  "fuel_type": "flex",
  "transmission": "automatic",
  "price": 85000.00,
  "description": "Excelente estado",
  "is_available": true,
  "brand_id": 1,
  "owner_id": 1,
  "created_at": "2023-01-01T00:00:00",
  "update_at": "2023-01-01T00:00:00",
  "brand": {
    "id": 1,
    "name": "Volkswagen",
    "description": "Fabricante alemão de veículos",
    "is_active": true,
    "created_at": "2023-01-01T00:00:00",
    "update_at": "2023-01-01T00:00:00"
  },
  "owner": {
    "id": 1,
    "username": "joaosilva",
    "email": "joao@example.com",
    "created_at": "2023-01-01T00:00:00",
    "update_at": "2023-01-01T00:00:00"
  }
}
```

#### Erros Possíveis
- 400: Placa já em uso, marca ou proprietário não encontrado

### Listar Carros
- **Endpoint**: `GET /api/v1/cars/`
- **Descrição**: Retorna uma lista de carros do proprietário autenticado
- **Autenticação**: JWT Bearer Token necessário

#### Parâmetros de Query
- `offset` (opcional): Número de registros para pular (padrão: 0)
- `limit` (opcional): Limite de registros (padrão: 100, máximo: 100)
- `search` (opcional): Buscar por modelo, cor ou placa
- `brand_id` (opcional): Filtrar por marca
- `owner_id` (opcional): Filtrar por proprietário
- `fuel_type` (opcional): Filtrar por tipo de combustível
- `transmission` (opcional): Filtrar por transmissão
- `is_available` (opcional): Filtrar por disponibilidade
- `min_price` (opcional): Preço mínimo
- `max_price` (opcional): Preço máximo

#### Exemplo de Requisição
```bash
curl -X GET "http://localhost:8000/api/v1/cars/?offset=0&limit=10&search=golf&is_available=true&min_price=50000&max_price=100000" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

#### Exemplo de Resposta (200 OK)
```json
{
  "cars": [
    {
      "id": 1,
      "model": "Golf",
      "factory_year": 2020,
      "model_year": 2021,
      "color": "Branco",
      "plate": "ABC1D23",
      "fuel_type": "flex",
      "transmission": "automatic",
      "price": 85000.00,
      "description": "Excelente estado",
      "is_available": true,
      "brand_id": 1,
      "owner_id": 1,
      "created_at": "2023-01-01T00:00:00",
      "update_at": "2023-01-01T00:00:00",
      "brand": {
        "id": 1,
        "name": "Volkswagen",
        "description": "Fabricante alemão de veículos",
        "is_active": true,
        "created_at": "2023-01-01T00:00:00",
        "update_at": "2023-01-01T00:00:00"
      },
      "owner": {
        "id": 1,
        "username": "joaosilva",
        "email": "joao@example.com",
        "created_at": "2023-01-01T00:00:00",
        "update_at": "2023-01-01T00:00:00"
      }
    }
  ],
  "offset": 0,
  "limit": 10
}
```

### Buscar Carro por ID
- **Endpoint**: `GET /api/v1/cars/{car_id}`
- **Descrição**: Retorna os detalhes de um carro específico
- **Autenticação**: JWT Bearer Token necessário

#### Parâmetros
- `car_id`: ID do carro

#### Exemplo de Requisição
```bash
curl -X GET "http://localhost:8000/api/v1/cars/1" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

#### Exemplo de Resposta (200 OK)
```json
{
  "id": 1,
  "model": "Golf",
  "factory_year": 2020,
  "model_year": 2021,
  "color": "Branco",
  "plate": "ABC1D23",
  "fuel_type": "flex",
  "transmission": "automatic",
  "price": 85000.00,
  "description": "Excelente estado",
  "is_available": true,
  "brand_id": 1,
  "owner_id": 1,
  "created_at": "2023-01-01T00:00:00",
  "update_at": "2023-01-01T00:00:00",
  "brand": {
    "id": 1,
    "name": "Volkswagen",
    "description": "Fabricante alemão de veículos",
    "is_active": true,
    "created_at": "2023-01-01T00:00:00",
    "update_at": "2023-01-01T00:00:00"
  },
  "owner": {
    "id": 1,
    "username": "joaosilva",
    "email": "joao@example.com",
    "created_at": "2023-01-01T00:00:00",
    "update_at": "2023-01-01T00:00:00"
  }
}
```

#### Erros Possíveis
- 403: Permissão negada (usuário não é o proprietário do carro)
- 404: Carro não encontrado

### Atualizar Carro
- **Endpoint**: `PUT /api/v1/cars/{car_id}`
- **Descrição**: Atualiza os dados de um carro
- **Autenticação**: JWT Bearer Token necessário

#### Parâmetros
- `car_id`: ID do carro
- Corpo da requisição (campos opcionais):
```json
{
  "model": "string",
  "factory_year": "integer",
  "model_year": "integer",
  "color": "string",
  "plate": "string",
  "fuel_type": "string",
  "transmission": "string",
  "price": "decimal",
  "description": "string",
  "is_available": "boolean",
  "brand_id": "integer",
  "owner_id": "integer"
}
```

#### Exemplo de Requisição
```bash
curl -X PUT "http://localhost:8000/api/v1/cars/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -d '{
    "price": 82000.00,
    "is_available": false
  }'
```

#### Exemplo de Resposta (200 OK)
```json
{
  "id": 1,
  "model": "Golf",
  "factory_year": 2020,
  "model_year": 2021,
  "color": "Branco",
  "plate": "ABC1D23",
  "fuel_type": "flex",
  "transmission": "automatic",
  "price": 82000.00,
  "description": "Excelente estado",
  "is_available": false,
  "brand_id": 1,
  "owner_id": 1,
  "created_at": "2023-01-01T00:00:00",
  "update_at": "2023-01-02T00:00:00",
  "brand": {
    "id": 1,
    "name": "Volkswagen",
    "description": "Fabricante alemão de veículos",
    "is_active": true,
    "created_at": "2023-01-01T00:00:00",
    "update_at": "2023-01-01T00:00:00"
  },
  "owner": {
    "id": 1,
    "username": "joaosilva",
    "email": "joao@example.com",
    "created_at": "2023-01-01T00:00:00",
    "update_at": "2023-01-01T00:00:00"
  }
}
```

#### Erros Possíveis
- 400: Placa já em uso, marca ou proprietário não encontrado
- 403: Permissão negada (usuário não é o proprietário do carro)
- 404: Carro não encontrado

### Deletar Carro
- **Endpoint**: `DELETE /api/v1/cars/{car_id}`
- **Descrição**: Remove um carro
- **Autenticação**: JWT Bearer Token necessário

#### Parâmetros
- `car_id`: ID do carro

#### Exemplo de Requisição
```bash
curl -X DELETE "http://localhost:8000/api/v1/cars/1" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

#### Exemplo de Resposta (204 No Content)

#### Erros Possíveis
- 403: Permissão negada (usuário não é o proprietário do carro)
- 404: Carro não encontrado

## Endpoint de Health Check

### Verificar Status da Aplicação
- **Endpoint**: `GET /health_check`
- **Descrição**: Retorna o status da aplicação
- **Autenticação**: Pública

#### Exemplo de Requisição
```bash
curl -X GET "http://localhost:8000/health_check"
```

#### Exemplo de Resposta (200 OK)
```json
{
  "status": "ok"
}
```

## Headers Comuns

### Headers de Requisição
- `Authorization: Bearer {token}` - Para endpoints protegidos
- `Content-Type: application/json` - Para requisições com corpo JSON

### Headers de Resposta
- `Content-Type: application/json` - Tipo de conteúdo das respostas