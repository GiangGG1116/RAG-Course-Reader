# ===== base =====
FROM python:3.10-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app


# Cài deps hệ thống tối thiểu
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl git && \
    rm -rf /var/lib/apt/lists/*


# ===== deps =====
FROM base AS deps
COPY requirements.txt .
# Tạo cache layer riêng cho pip
RUN pip install --no-cache-dir -r requirements.txt


# ===== runtime =====
FROM base AS runtime
# Tạo user không phải root
RUN useradd -m -u 1000 appuser
USER appuser


# Copy site-packages từ layer deps
COPY --from=deps /usr/local/lib/python3.10 /usr/local/lib/python3.10
COPY --from=deps /usr/local/bin /usr/local/bin


# Copy code
COPY --chown=appuser:appuser . .
ENV PYTHONPATH=/app


# Thư mục persist
RUN mkdir -p /app/storage /app/data && \
    chmod -R 755 /app/storage /app/data


EXPOSE 8000
CMD ["bash","-lc","uvicorn src.api:app --host 0.0.0.0 --port 8000 --workers 2"]