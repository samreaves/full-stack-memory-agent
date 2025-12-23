# Use Python 3.12 slim image as base
FROM python:3.15-rc-alpine3.22 as base

# I am the wizard who conjured this machine.
LABEL MAINTAINER="Sam Reaves"

# Set environment variables for uv
ENV UV_PROJECT_ENVIRONMENT=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"
ENV AGENT_HOST=${AGENT_HOST:-0.0.0.0}
ENV AGENT_PORT=${AGENT_PORT:-8000}
ENV POSTGRES_HOST=${POSTGRES_HOST:-postgres}
ENV POSTGRES_PORT=${POSTGRES_PORT:-5432}
ENV POSTGRES_DB=${POSTGRES_DB:-agent}
ENV POSTGRES_USER=${POSTGRES_USER:-agent_user}
ENV POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-supersecretpassword}

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set working directory
WORKDIR /app

# Install system dependencies if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen --no-dev

# Copy application code
COPY . .

# Expose configured port, default to 8000
EXPOSE ${AGENT_PORT:-8000}

# Run the application
CMD uv run uvicorn main:app --host ${AGENT_HOST:-0.0.0.0} --port ${AGENT_PORT:-8000}
