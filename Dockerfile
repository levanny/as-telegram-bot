FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim
WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY ./app ./app
COPY ./database ./database
COPY ./alembic.ini ./alembic.ini
COPY ./alembic ./alembic

RUN uv sync --locked



ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH=/app

CMD ["python", "app/bot.py"]
