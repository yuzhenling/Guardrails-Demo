# syntax=docker/dockerfile:1.7
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    NV_GUARDRAILS_LOG_LEVEL=DEBUG

WORKDIR /app

# Build tools are needed for some Python dependencies without prebuilt wheels.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && pip install uv

COPY pyproject.toml uv.lock ./


ENV UV_HTTP_TIMEOUT=300
ENV UV_DEFAULT_INDEX="https://pypi.tuna.tsinghua.edu.cn/simple"
#ENV UV_EXTRA_INDEX_URL="https://mirrors.aliyun.com/pypi/simple/"
ENV UV_CACHE_DIR=/root/.cache/uv2
ENV UV_CONCURRENT_DOWNLOADS=4

RUN --mount=type=cache,id=uv-cache-v2,target=/root/.cache/uv2 \
    uv sync --frozen -v

COPY . .

EXPOSE 8000

CMD ["uv", "run", "nemoguardrails", "server", "--config=config", "--port=8000"]
