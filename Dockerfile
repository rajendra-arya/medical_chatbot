FROM python:3.10-slim-bookworm AS builder

WORKDIR /build

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN python3 -m pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

FROM python:3.10-slim-bookworm AS runner
WORKDIR /app

COPY --from=builder /usr/local /usr/local
COPY app.py ./
COPY src ./src
COPY templates ./templates
COPY static ./static

RUN groupadd --system appuser \
    && useradd --system --gid appuser --home-dir /app appuser \
    && chown -R appuser:appuser /app

USER appuser
EXPOSE 8080

CMD ["python3", "app.py"]
