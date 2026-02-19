FROM python:3.13.11-alpine3.22

SHELL ["/bin/sh", "-o", "pipefail", "-c"]
ENV POETRY_VERSION=2.3.2 \
    PATH="/root/.local/bin:$PATH"

RUN apk add curl && \
    curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app

COPY . .
RUN poetry install --without dev

CMD ["poetry", "run", "fastapi", "dev", "car_api/app.py", "--host", "0.0.0.0"]