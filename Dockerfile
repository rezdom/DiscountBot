FROM python:3.12.3-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYCODE 1
ENV PYTHONNUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "alembic upgrade head && python3 -m src.main"]