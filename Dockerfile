FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --locked

COPY ./app ./app
COPY ./database ./database
COPY ./alembic.ini ./alembic.ini
COPY ./alembic ./alembic

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH=/app

CMD ["python", "-m", "app.main"]
