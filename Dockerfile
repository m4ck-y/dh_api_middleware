FROM python:3.13-bookworm

COPY --from=ghcr.io/astral-sh/uv:0.8.8 /uv /uvx /bin/

WORKDIR /app

# Cache layer: dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --locked

# Application layer: source code
COPY . .

# Security: run as non-root user
RUN useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
