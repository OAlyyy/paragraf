FROM python:3.12-slim
RUN pip install --no-cache-dir uv==0.11.32
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project
COPY . .
RUN uv sync --frozen --no-dev
CMD ["sh", "-c", "uv run --no-sync python -m paragraf.migrate && uv run --no-sync uvicorn paragraf.api.main:app --host 0.0.0.0 --port 8000"]
