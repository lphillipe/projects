FROM python:3.13.11

ARG POETRY_VERSION=2.3.2

RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=${POETRY_VERSION} python3 -

ENV PATH="/root/.local/bin:$PATH"