# Deploy

Este documento fornece instruções para implantar a API de Gerenciamento de Carros em diferentes ambientes (desenvolvimento, staging, produção).

## Visão Geral

A API pode ser implantada em diversos ambientes e plataformas. Este guia cobre as opções mais comuns e as melhores práticas para cada cenário.

## Pré-requisitos para Deploy

### Servidor
- Sistema operacional Linux (recomendado)
- Python 3.13 ou superior
- Gerenciador de processos (como systemd ou supervisor)
- Proxy reverso (como Nginx)

### Recursos
- Memória RAM: 1GB ou mais
- Espaço em disco: 500MB livres
- Conexão de rede estável

## Configurações de Produção

### Variáveis de Ambiente

Certifique-se de configurar as variáveis de ambiente apropriadas para produção:

```
DATABASE_URL=postgresql+asyncpg://usuario:senha@localhost:5432/nome_do_banco
JWT_SECRET_KEY=sua_chave_super_secreta_segura_e_unica_para_producao
JWT_EXPIRATION_MINUTES=15
```

### Banco de Dados

Para produção, recomenda-se usar PostgreSQL em vez de SQLite:

```
DATABASE_URL=postgresql+asyncpg://usuario:senha@localhost:5432/car_api_prod
```

## Opções de Deploy

### 1. Deploy em Servidor Próprio

#### Configuração do Servidor

1. Atualize o sistema:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. Instale dependências:
   ```bash
   sudo apt install python3.13 python3.13-venv python3.13-dev build-essential nginx postgresql postgresql-contrib supervisor git -y
   ```

3. Crie um usuário para a aplicação:
   ```bash
   sudo useradd -m -s /bin/bash carapi
   sudo su - carapi
   ```

#### Instalação da Aplicação

1. Clone o repositório:
   ```bash
   git clone <URL_DO_REPOSITORIO> ~/car_api
   cd ~/car_api
   ```

2. Crie ambiente virtual:
   ```bash
   python3.13 -m venv venv
   source venv/bin/activate
   ```

3. Instale Poetry e dependências:
   ```bash
   pip install poetry
   poetry install --only=main
   ```

4. Configure o ambiente:
   ```bash
   cp .env.example .env
   # Edite .env com as configurações de produção
   ```

5. Execute migrações:
   ```bash
   poetry run alembic upgrade head
   ```

#### Execução com Gunicorn

1. Instale Gunicorn:
   ```bash
   poetry add gunicorn
   ```

2. Execute a aplicação:
   ```bash
   gunicorn car_api.app:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

#### Configuração do Supervisor

Crie um arquivo de configuração do Supervisor em `/etc/supervisor/conf.d/car_api.conf`:

```ini
[program:car_api]
command=/home/carapi/car_api/venv/bin/gunicorn car_api.app:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 127.0.0.1:8000
directory=/home/carapi/car_api
user=carapi
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/car_api.log
environment=PATH="/home/carapi/car_api/venv/bin"
```

Recarregue o Supervisor:
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start car_api
```

#### Configuração do Nginx

Crie um arquivo de configuração do Nginx em `/etc/nginx/sites-available/car_api`:

```nginx
server {
    listen 80;
    server_name seu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Ative o site:
```bash
sudo ln -s /etc/nginx/sites-available/car_api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 2. Deploy com Docker

#### Dockerfile

Crie um Dockerfile na raiz do projeto:

```dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --only=main

COPY . .

EXPOSE 8000

CMD ["gunicorn", "car_api.app:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

#### Docker Compose

Crie um arquivo `docker-compose.yml`:

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: car_api_prod
      POSTGRES_USER: carapi
      POSTGRES_PASSWORD: strongpassword
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  api:
    build: .
    environment:
      DATABASE_URL: postgresql+asyncpg://carapi:strongpassword@db:5432/car_api_prod
      JWT_SECRET_KEY: sua_chave_super_secreta
    ports:
      - "8000:8000"
    depends_on:
      - db
    command: >
      sh -c "poetry run alembic upgrade head &&
             gunicorn car_api.app:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000"

volumes:
  postgres_data:
```

Execute com:
```bash
docker-compose up -d
```

### 3. Deploy em Plataforma em Nuvem

#### Heroku

1. Crie um arquivo `Procfile`:
   ```
   web: gunicorn car_api.app:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
   ```

2. Crie um app no Heroku:
   ```bash
   heroku create nome-do-seu-app
   ```

3. Defina as configurações:
   ```bash
   heroku config:set DATABASE_URL=...
   heroku config:set JWT_SECRET_KEY=...
   ```

4. Faça deploy:
   ```bash
   git push heroku main
   ```

#### Render

1. Crie uma conta em https://render.com
2. Conecte seu repositório GitHub
3. Crie um serviço Web Service
4. Configure as variáveis de ambiente
5. Renderizará automaticamente após pushes

#### Railway

1. Crie uma conta em https://railway.app
2. Importe seu repositório
3. Configure as variáveis de ambiente
4. O deploy ocorre automaticamente

## Considerações de Segurança

### HTTPS

Configure HTTPS usando Let's Encrypt:

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d seu-dominio.com
```

### Firewall

Configure o firewall para permitir apenas as portas necessárias:

```bash
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

### Hardening

- Mantenha o sistema atualizado
- Use chaves SSH para acesso
- Configure logs adequados
- Monitore acessos suspeitos

## Monitoramento

### Logs

Configure logging adequado:

```bash
# Visualizar logs da aplicação
sudo tail -f /var/log/car_api.log

# Visualizar logs do Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Métricas

Considere integrar soluções de monitoramento como:

- Prometheus + Grafana
- DataDog
- New Relic

## Estratégias de Deploy

### Blue-Green Deploy

Implemente deploy azul-verde para zero downtime:

1. Mantenha duas cópias idênticas da aplicação
2. Roteie tráfego para uma versão (verde)
3. Implemente atualizações na outra versão (azul)
4. Alterne o roteamento quando pronta

### Canary Releases

Implemente releases canário para mitigar riscos:

1. Redirecione uma pequena porcentagem de tráfego para nova versão
2. Monitore métricas e logs
3. Gradualmente aumente o tráfego se tudo estiver bem
4. Reverta se problemas forem detectados

## Rollback

Tenha um plano de rollback:

1. Mantenha backups do banco de dados
2. Armazene versões anteriores da aplicação
3. Documente o processo de reversão
4. Teste o processo de rollback regularmente

## Melhores Práticas

### Antes do Deploy

- Execute todos os testes
- Verifique a cobertura de código
- Realize revisão de código
- Atualize a documentação

### Durante o Deploy

- Monitore métricas críticas
- Verifique logs em tempo real
- Teste manualmente funcionalidades principais
- Comunique equipe sobre o deploy

### Após o Deploy

- Verifique saúde da aplicação
- Monitore métricas de desempenho
- Observe logs de erro
- Colete feedback dos usuários

## Troubleshooting

### Problemas Comuns

1. **Permissão de arquivo**: Verifique permissões do usuário do serviço
2. **Conexão com banco de dados**: Confirme credenciais e conectividade
3. **Timeouts**: Ajuste configurações de timeout do proxy
4. **Erros de memória**: Ajuste número de workers ou aloque mais memória

### Verificação de Saúde

Endpoint para verificação de saúde da aplicação:
```
GET /health_check
```

### Comandos Úteis

```bash
# Verificar status do serviço
sudo systemctl status car_api

# Reiniciar aplicação
sudo supervisorctl restart car_api

# Verificar uso de recursos
htop
df -h
du -sh ~/car_api
```

## Continuos Integration/Deployment (CI/CD)

Considere implementar pipelines CI/CD usando:

- GitHub Actions
- GitLab CI/CD
- Jenkins
- CircleCI

Exemplo de pipeline básico:

1. Rodar testes em cada push
2. Verificar qualidade do código
3. Fazer build da imagem Docker
4. Fazer deploy em ambiente de staging
5. Após aprovação, fazer deploy em produção