FROM python:3.12-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY pyproject.toml .
COPY uv.lock .
RUN uv sync && . .venv/bin/activate

COPY main.py .
COPY src src

CMD ["uv", "run", "streamlit", "run", "main.py", "--server.port", "3000"]
