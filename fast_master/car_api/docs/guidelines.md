# Guidelines e Padrões

Este documento define os padrões e diretrizes de desenvolvimento para manter a consistência e qualidade do código na API de Gerenciamento de Carros.

## Padrões de Codificação

### Python
- **PEP 8**: Siga as convenções do PEP 8 para estilo de código Python
- **Tipagem**: Use tipagem estática com type hints sempre que possível
- **Nomenclatura**: Use nomes descritivos e consistentes para variáveis, funções e classes
- **Comprimento de Linha**: Limite as linhas a 79 caracteres (configurado no `pyproject.toml`)

### Importações
- Ordene as importações seguindo o padrão: bibliotecas padrão → bibliotecas de terceiros → módulos locais
- Separe cada grupo com uma linha em branco
- Evite importações globais desnecessárias

### Docstrings e Comentários
- Use docstrings para todas as funções, métodos e classes
- Prefira docstrings no estilo Google ou NumPy
- Comente apenas quando necessário para explicar decisões complexas
- Evite comentários óbvios

## Estrutura de Código

### Organização de Pastas
- `car_api/`: Código-fonte principal
- `car_api/core/`: Componentes centrais (configurações, banco de dados, segurança)
- `car_api/models/`: Modelos do SQLAlchemy
- `car_api/schemas/`: Esquemas Pydantic para validação
- `car_api/routers/`: Roteadores FastAPI
- `tests/`: Testes automatizados
- `docs/`: Documentação

### Classes e Funções
- Mantenha funções pequenas e com responsabilidade única
- Use classes para agrupar funcionalidades relacionadas
- Prefira funções puras quando possível
- Evite funções com muitos parâmetros (mais de 5)

## Padrões de Projeto

### FastAPI
- Use Pydantic para validação de entrada e saída de dados
- Implemente dependências para injeção de dependência
- Utilize decoradores do FastAPI para documentação automática
- Siga o padrão REST para criação de endpoints

### SQLAlchemy
- Use modelos declarativos
- Implemente relacionamentos claros entre tabelas
- Prefira consultas assíncronas com `async def`
- Use sessões assíncronas (`AsyncSession`)

### Pydantic
- Defina esquemas de entrada e saída separadamente
- Use validadores personalizados quando necessário
- Implemente `ConfigDict(from_attributes=True)` para compatibilidade com SQLAlchemy

## Segurança

### Autenticação e Autorização
- Use tokens JWT para autenticação
- Implemente middleware de segurança
- Valide tokens em todas as rotas protegidas
- Use hashing seguro para senhas (Argon2 via pwdlib)

### Validação de Entrada
- Valide todos os dados recebidos
- Use Pydantic para validação automática
- Implemente sanitização de entradas
- Evite SQL injection com SQLAlchemy

### Proteção contra ataques
- Implemente rate limiting para endpoints sensíveis
- Use HTTPS em produção
- Evite exposição de informações sensíveis
- Sanitize dados antes de retornar ao cliente

## Qualidade de Código

### Linting
- Use Ruff para verificação de estilo e erros
- Execute `poetry run task lint` para verificar problemas
- Execute `poetry run task pre_format` para corrigir automaticamente
- Execute `poetry run task format` para formatar o código

### Formatação
- Use aspas simples para strings (configurado no `pyproject.toml`)
- Mantenha consistência no estilo de formatação
- Use formatação automática com Ruff

### Testes
- Escreva testes unitários para todas as funções críticas
- Use Pytest para execução de testes
- Mantenha cobertura de código alta
- Teste casos de erro e sucesso

## Versionamento

### Git
- Use mensagens de commit claras e descritivas
- Siga convenções de commit como conventional commits
- Use branches para desenvolvimento de features
- Evite commits de código quebrado

### Commits
- Escreva mensagens de commit em português ou inglês
- Use o formato imperativo: "Add feature" em vez de "Added feature"
- Descreva o que e por que algo foi feito
- Divida mudanças grandes em commits menores e lógicos

## Documentação

### Código
- Documente funções e classes com docstrings
- Explique decisões complexas com comentários
- Mantenha a documentação atualizada com o código

### API
- Use decoradores do FastAPI para documentação automática
- Forneça exemplos de requisição e resposta
- Documente parâmetros, cabeçalhos e status codes
- Atualize a documentação quando alterar endpoints

## Performance

### Consultas ao Banco de Dados
- Use eager loading para evitar N+1 queries
- Otimize consultas com filtros e índices
- Prefira consultas assíncronas
- Use paginação para resultados grandes

### Recursos
- Minimize o uso de memória
- Evite operações pesadas na thread principal
- Use caching quando apropriado
- Monitore o desempenho da aplicação

## Boas Práticas

### Tratamento de Erros
- Use exceções HTTP apropriadas do FastAPI
- Forneça mensagens de erro claras e úteis
- Registre erros para análise posterior
- Evite expor detalhes internos nos erros

### Manutenibilidade
- Escreva código legível e autoexplicativo
- Evite duplicação de código
- Use constantes para valores mágicos
- Refatore código complexo regularmente

### Colaboração
- Revise código de colegas
- Use pull requests para mudanças significativas
- Mantenha discussões técnicas construtivas
- Siga os padrões estabelecidos pela equipe