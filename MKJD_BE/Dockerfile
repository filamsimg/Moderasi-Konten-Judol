FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements-core.txt requirements-ml.txt requirements.txt ./
RUN pip install --no-cache-dir -r requirements-core.txt

COPY alembic ./alembic
COPY alembic.ini ./
COPY app ./app
COPY scripts ./scripts

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
