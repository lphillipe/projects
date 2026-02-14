# Contribuição

Este documento fornece diretrizes para contribuir com o projeto API de Gerenciamento de Carros. Sua contribuição é bem-vinda e importante para o crescimento e melhoria contínua do projeto.

## Como Contribuir

### Primeiros Passos

1. **Fork o repositório**: Clique no botão "Fork" no topo da página do repositório original

2. **Clone seu fork**:
   ```bash
   git clone https://github.com/seu-usuario/car_api.git
   cd car_api
   ```

3. **Crie uma branch para sua feature ou correção**:
   ```bash
   git checkout -b feature/sua-nova-feature
   # ou
   git checkout -b fix/bug-corrigido
   ```

4. **Faça suas alterações** seguindo as diretrizes deste documento

5. **Teste suas alterações** (quando testes estiverem disponíveis)

6. **Commit suas alterações**:
   ```bash
   git add .
   git commit -m "Descrição clara e concisa das alterações"
   ```

7. **Envie para seu fork**:
   ```bash
   git push origin feature/sua-nova-feature
   ```

8. **Abra um Pull Request** no repositório original

## Tipos de Contribuições

### Código
- Correções de bugs
- Novas funcionalidades
- Melhorias de desempenho
- Refatorações

### Documentação
- Correções de erros de digitação
- Explicações mais claras
- Exemplos adicionais
- Traduções

### Testes
- Adição de testes unitários
- Testes de integração
- Casos de teste para cenários de borda

### Relatórios de Bugs
- Relatórios detalhados de bugs
- Sugestões de melhorias
- Solicitações de novas funcionalidades

## Diretrizes de Código

### Estilo de Codificação
- Siga as diretrizes descritas em [Guidelines e Padrões](guidelines.md)
- Use PEP 8 como referência para estilo Python
- Mantenha consistência com o código existente
- Use nomes descritivos para variáveis, funções e classes

### Commits
- Escreva mensagens de commit claras e descritivas
- Use o tempo verbal imperativo: "Add feature" em vez de "Added feature"
- Limite a primeira linha a 50 caracteres
- Explique o quê e por que algo foi feito

### Branches
- Use nomes descritivos para branches
- Mantenha branches focadas em uma única tarefa
- Evite misturar diferentes tipos de alterações

## Processo de Revisão

### Pull Requests
- Descreva claramente as alterações feitas
- Inclua contexto sobre por que as alterações são necessárias
- Liste etapas para testar as alterações manualmente
- Referencie issues relevantes (se aplicável)

### Revisões
- Seja receptivo ao feedback
- Faça alterações solicitadas pelas revisões
- Explique decisões de design quando necessário
- Agradeça pelos comentários e sugestões

## Ambiente de Desenvolvimento

Siga as instruções em [Guia de Desenvolvimento](development.md) para configurar seu ambiente de desenvolvimento.

### Configuração Inicial
```bash
# Instale dependências
poetry install

# Ative o ambiente virtual
poetry shell

# Configure variáveis de ambiente
cp .env.example .env
# Edite .env com configurações apropriadas

# Execute migrações
poetry run alembic upgrade head
```

### Verificação de Código
Antes de fazer commit, verifique e formate seu código:
```bash
# Verificar problemas
poetry run task lint

# Formatar automaticamente
poetry run task pre_format
```

## Recursos para Contribuidores

### Comunicação
- Use issues para relatar bugs e sugerir melhorias
- Participe de discussões em pull requests
- Entre em contato com os mantenedores se tiver dúvidas

### Aprendizado
- Leia a documentação existente
- Explore o código para entender a arquitetura
- Consulte a documentação das tecnologias usadas:
  - [FastAPI](https://fastapi.tiangolo.com/)
  - [SQLAlchemy](https://docs.sqlalchemy.org/)
  - [Pydantic](https://docs.pydantic.dev/)

## Boas Práticas

### Código Limpo
- Escreva código legível e bem documentado
- Evite duplicação de código
- Use funções e classes com responsabilidade única
- Comente decisões complexas ou não óbvias

### Segurança
- Siga as práticas de segurança descritas em [Autenticação e Segurança](authentication_security.md)
- Valide todas as entradas de usuário
- Use SQLAlchemy para evitar SQL injection
- Implemente controle de acesso adequado

### Performance
- Considere o impacto de performance de suas alterações
- Use consultas eficientes ao banco de dados
- Implemente paginação para listagens grandes
- Evite N+1 queries

## Código de Conduta

Ao contribuir com este projeto, você concorda em seguir nosso código de conduta:

- Seja respeitoso com outros colaboradores
- Ofereça feedback construtivo
- Seja acolhedor com iniciantes
- Foque na qualidade técnica e na utilidade do código
- Evite comportamentos inapropriados ou discriminatórios

## Reconhecimento

Todos os contribuidores são reconhecidos em nosso arquivo de changelog e na documentação de lançamentos. Sua contribuição é valiosa para o projeto!

## Dúvidas

Se você tiver dúvidas sobre como contribuir:

1. Leia toda a documentação do projeto
2. Verifique issues abertos e fechados
3. Abra um issue para perguntas
4. Entre em contato com os mantenedores

## Templates

### Template para Issues
```
**Descrição**
Breve descrição do problema ou solicitação.

**Passos para reproduzir (se for bug)**
1. Faça isso
2. Então faça aquilo
3. Veja o erro

**Comportamento esperado**
Descrição do que deveria acontecer.

**Comportamento atual**
Descrição do que realmente acontece.

**Contexto adicional**
Qualquer informação adicional que possa ajudar.
```

### Template para Pull Requests
```
**Descrição**
Explicação do que foi alterado e por que.

**Tipos de alterações**
- [ ] Correção de bug
- [ ] Nova funcionalidade
- [ ] Quebra de compatibilidade
- [ ] Documentação

**Checklist**
- [ ] Minhas alterações não quebram o código existente
- [ ] Adicionei testes que cobrem minhas alterações
- [ ] Atualizei a documentação (se necessário)
- [ ] Minhas alterações precisam de atualização de documentação
```

Agradecemos por considerar contribuir com o projeto API de Gerenciamento de Carros!