FROM python:3.14-slim AS builder

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

COPY --from=ghcr.io/astral-sh/uv:0.12.10 /uv /uvx /bin/

# Change the working directory to the `app` directory
WORKDIR /app

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

# Copy the project into the image
COPY . /app

# Sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

# build

WORKDIR /app/pages

RUN apt-get update && apt-get install -y git
RUN uv run mkdocs build

FROM caddy:2.11.4-alpine AS server

COPY --from=builder /app/pages/site /usr/share/caddy