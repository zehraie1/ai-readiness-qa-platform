# syntax=docker/dockerfile:1
# Single-origin image: FastAPI serves the API and the built React SPA (ADR-011).

FROM node:24-alpine AS web
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci --no-audit --no-fund
COPY frontend/ ./
RUN npm run build

FROM python:3.12-slim AS app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /app
RUN useradd --create-home --uid 10001 appuser
COPY backend/requirements.txt backend/requirements.txt
RUN pip install -r backend/requirements.txt
COPY backend/alembic.ini backend/alembic.ini
COPY backend/app backend/app
COPY database/migrations database/migrations
COPY database/seed database/seed
COPY scripts/start.sh scripts/start.sh
COPY --from=web /app/frontend/dist frontend/dist

ENV APP_ENV=demo \
    SERVE_FRONTEND=true \
    FRONTEND_DIST=/app/frontend/dist \
    COOKIE_SECURE=true \
    PORT=8000
USER appuser
EXPOSE 8000
CMD ["sh", "/app/scripts/start.sh"]
