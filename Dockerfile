# ---- Stage 1: build the frontend as a static export ----
FROM node:20-slim AS frontend-builder
WORKDIR /frontend
COPY frontend/package.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build
# output: "export" in next.config.js produces /frontend/out (fully static HTML/JS/CSS)

# ---- Stage 2: backend + serves the static frontend on the same port ----
FROM python:3.12-slim
WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .
COPY --from=frontend-builder /frontend/out ./static

EXPOSE 8000
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
